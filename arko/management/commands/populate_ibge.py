import logging
from django.core.management import BaseCommand
from django.db import transaction
from arko.models import District,Municipality, Region, State
from arko.services import IBGEApiClient

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database with States, Municipalities, and Dristricts from IBGE API.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client =IBGEApiClient()

    @transaction.atomic
    def handle(self, *args, **options):
        """"
        Main execution method for the command.
        """
        logger.info('Starting import of IBGE data...') 
        try:
            self._import_regions_and_state()
            self._bulk_import_municipalities()
            self._bulk_import_districts()
        except Exception as e:
            logger.error(f"A critical error occured during the import process: {e}", exc_info=True)
            logger.warning('Operation cancelled. No changes were saved to the database.')
            return

        logger.info('Import completed successfully!')

    def _import_regions_and_state(self):
        """
        Imports Regions and States. 
        """
        logger.info('Importing Regions and States...')
        states_data = self.client.get_states()

        regions_created = 0
        states_created = 0

        for data in states_data:
            region_data = data.regiao

            try:
                _, created = Region.objects.get_or_create(
                id = region_data.id,
                defaults={'sigla': region_data.sigla, 'nome': region_data.nome}
                )
                regions_created+=1
            except Exception as e:
                logging.ERROR(f"Error in create region: {e}")

            try:
                region_obj = Region.objects.get(id=region_data.id)

                _, created = State.objects.get_or_create(
                    id=data.id,
                    defaults={'sigla': data.id, 'nome': data.nome, 'regiao': region_obj}
                )   

                states_created+=1
            except Exception as e:
                logging.ERROR(f"Errir ub create State {e}")

            
        logger.info(f"{regions_created} new regions and {states_created} new states processed.")

    def _bulk_import_municipalities(self):
        """
        Bulk imports all municipalities, designed for high performance.
        1. Fetches all municipality data in a single API call.
        2. Fetches existing data from the DB into memory to avoid loops of queries.
        3. Inserts all new municipalities in a single bulk_create query.
        """
        logger.info('Bulk importing Municipalities...')
        
        municipalities_data = self.client.get_all_municipalities()

        states_map = {s.id: s for s in State.objects.all()}
        existing_ids = set(Municipality.objects.values_list('id', flat=True))

        municipalities_to_create = []
        for data in municipalities_data:
            if data.id in existing_ids:
                continue

            if not data.microrregiao:
                logger.warning(f"Municipality {data.id} ({data.nome}) is missing microrregiao data from API. Skipping.")
                continue

            state_id = data.microrregiao.mesorregiao.UF.id
            state_instance = states_map.get(state_id)
        
            if state_instance:
                municipalities_to_create.append(
                    Municipality(
                        id=data.id,
                        nome=data.nome,
                        estado=state_instance
                    )
                )   

        if municipalities_to_create:
            Municipality.objects.bulk_create(municipalities_to_create, batch_size=1000)
        
        logger.info(f'{len(municipalities_to_create)} new municipalities created.')

    def _bulk_import_districts(self):
        """
        Bulk imports all districts.
        """
        logger.info('Bulk importing Districts...')
        districts_data = self.client.get_all_districts()
        
        municipalities_map = {m.id: m for m in Municipality.objects.all()}
        existing_ids = set(District.objects.values_list('id', flat=True))
        
        districts_to_create = []
        for data in districts_data:
            if data.id in existing_ids:
                continue

            municipality_id = data.municipio.id
            municipality_instance = municipalities_map.get(municipality_id)
            
            if municipality_instance:
                districts_to_create.append(
                    District(
                        id=data.id,
                        nome=data.nome,
                        municipio=municipality_instance
                    )
                )

        if districts_to_create:
            District.objects.bulk_create(districts_to_create, batch_size=1000)

        logger.info(f'{len(districts_to_create)} new districts created.') 

