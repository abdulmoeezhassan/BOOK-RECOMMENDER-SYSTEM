import yaml
import sys
from books_recommender.exception.exception_handler import AppException


def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns its contents as a dictionary.

    :param file_path: Path to the YAML file.
    :return: Dictionary containing the contents of the YAML file.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content
    except Exception as e:
        raise AppException(e, sys) from e
