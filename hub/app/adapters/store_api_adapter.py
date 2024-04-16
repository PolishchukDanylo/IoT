import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (List[ProcessedAgentData]): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        logging.info("GOT INTO save_data")
        headers = {"Content-Type": "application/json"}
        url = f"{self.api_base_url}/processed_agent_data"
        data = [json.loads(value) for value in processed_agent_data_batch]
        try:
            response = requests.post(url, headers=headers, json=data)
            logging.info(f"Response var: {response}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to save data: {e}")
            logging.info(f"Failed to save data:" , e)
            return False