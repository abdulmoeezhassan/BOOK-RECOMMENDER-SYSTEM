import os
import sys
import zipfile
from urllib.request import urlretrieve
from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration


class DataIngestion:
    def __init__(self, app_config: AppConfiguration = AppConfiguration()):
        """
        Initializes the DataIngestion process with the given configuration.
        """
        try:
            logging.info("=" * 20 + " Data Ingestion started " + "=" * 20)
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def download_data(self) -> str:
        """
        Downloads the dataset zip file from the specified URL.
        Returns:
            str: Path to the downloaded zip file.
        """
        try:
            dataset_url = self.data_ingestion_config.dataset_download_url
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir, exist_ok=True)

            zip_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(raw_data_dir, zip_file_name)

            logging.info(f"Downloading dataset from URL: {dataset_url}")
            urlretrieve(dataset_url, zip_file_path)
            logging.info(f"Data downloaded successfully to: {zip_file_path}")

            return zip_file_path
        except Exception as e:
            raise AppException(e, sys) from e

    def extract_data(self, zip_file_path: str) -> None:
        """
        Extracts the contents of the zip file into the specified directory.
        Args:
            zip_file_path (str): Path to the zip file to extract.
        """
        try:
            extract_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            logging.info(f"Extracted zip file: {zip_file_path} to directory: {extract_dir}")
        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_ingestion(self) -> None:
        """
        Coordinates the data ingestion process: downloading and extracting data.
        """
        try:
            zip_file_path = self.download_data()
            self.extract_data(zip_file_path)
            logging.info("=" * 20 + " Data Ingestion completed " + "=" * 20 + "\n")
        except Exception as e:
            raise AppException(e, sys) from e
