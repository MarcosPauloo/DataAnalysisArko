import logging
import pandas as pd
import zipfile
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from django.db import transaction
from arko.models import Company

logger = logging.getLogger(__name__)

COLUMN_NAMES = [
    'cnpj', 'razao_social', 'natureza_juridica', 'qualificacao_responsavel',
    'capital_social', 'porte_empresa', 'ente_federativo_responsavel'
]

class Command(BaseCommand):
    help = 'Populates the Company model from the official Receita Federal ZIP.'

    def add_arguments(self, parser):
        parser.add_argument('zip_file_path', type=str, help="The full path to the EmpresaX.zip file.")
    
    @transaction.atomic
    def handle(self, *args, **options):
        zip_file_path = options['zip_file_path']
        chunk_size = 50000

        logger.info(f"Starting company data import from {zip_file_path}...")

        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zf:
                csv_filename = next((name for name in zf.namelist() if 'EMPRECSV' in name.upper()), None)
                if not csv_filename:
                    raise FileNotFoundError("No 'EMPRESAS' CSV file found in the ZIP archive.")
                
                logger.info(f"Found CSV file in ZIP: {csv_filename}")
                with zf.open(csv_filename, 'r') as csv_file:
                    csv_reader = pd.read_csv(
                        csv_file,
                        header=None,
                        names=COLUMN_NAMES,
                        sep=';',
                        encoding='latin-1',
                        dtype=str,
                        chunksize=chunk_size
                    )

                    total_rows_processed = 0

                    for i, chunk in enumerate(csv_reader):
                        self.process_chunk(chunk)
                        total_rows_processed+=len(chunk)
                        logger.info(f"Processed chunk {i+1}... Total rows so far: {total_rows_processed}")
        except Exception as e:
            logger.error(f"A critial error occured: {e}", exc_info=True)
            raise
    
    logger.info(f"Successfully imported data for {Company.objects.count()} companies.")

    def process_chunk(self, chunk:pd.DataFrame):
        """Processes a single chunk of the DataFrame and performs a bulk upsert."""

        chunk['capital_social'] = chunk['capital_social'].str.replace(',', '.', regex=False)
        chunk['capital_social'] = pd.to_numeric(chunk['capital_social'], errors='coerce').fillna(0).astype(float)

        objects_to_upsert = []
        for _, row in chunk.iterrows():
            objects_to_upsert.append(Company(
                    cnpj=row['cnpj'],
                    razao_social=row['razao_social'],
                    natureza_juridica=row['natureza_juridica'],
                    qualificacao_responsavel=row['qualificacao_responsavel'],
                    capital_social=Decimal(row['capital_social']),
                    porte_empresa=row['porte_empresa'],
                    ente_federativo_responsavel=row['ente_federativo_responsavel']
                ))
        Company.objects.bulk_create(
            objects_to_upsert,
            update_conflicts=True,
            unique_fields=['cnpj'],
            update_fields=['razao_social', 'natureza_juridica', 'qualificacao_responsavel', 'capital_social', 'porte_empresa', 'ente_federativo_responsavel']
        )