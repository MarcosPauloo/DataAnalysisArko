import logging
import requests
from requests.exceptions import RequestException
from typing import List, Dict, Any
from pydantic import ValidationError

from .schema import StateSchema, MunicipalitySchema, DistrictSchema

IBGE_API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
DEFAULT_TIMEOUT = 15 ## seconds

logger = logging.getLogger(__name__)

class IBGEApiClient:
    """"
    A client to interact with the IBGE Locality API.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def _make_request(self, endpoint:str)-> List[Dict[str, Any]]:
        """Makes a request to a given endpoint."""
        url= f"{IBGE_API_URL}/{endpoint}"
        try:
            response=self.session.get(url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Error during API request to {url}: {e}", exc_info=True)
            raise
        except ValueError as e:
            logger.error(f"Error decoding JSON from {url}: {e}", exc_info=True)
            raise

    def get_states(self) -> List[StateSchema]:
        """Fetches and validates all states from the API."""
        response_data = self._make_request("estados?orderBy=nome")

        try:
            return [StateSchema.model_validate(item) for item in response_data]
        except ValidationError as e:
            logger.error(f"API response for States did not match schema: {e}") 
            raise
    def get_all_municipalities(self) -> List[MunicipalitySchema]:
        """Fetches and validates all municipalities."""
        response_data = self._make_request("municipios?orderBy=nome")
        
        try:
            return [MunicipalitySchema.model_validate(item) for item in response_data]
        except ValidationError as e:
            logger.error(f"API response for Municipalities did not match schema: {e}")
            raise
    def get_all_districts(self) -> List[DistrictSchema]:
        """Fetches and validates all districts."""
        response_data = self._make_request("distritos?orderBy=nome")
        try:
            return [DistrictSchema.model_validate(item) for item in response_data]
        except ValidationError as e:
            logger.error(f"API reponse for Districts did not match schema: {e}")
            raise

