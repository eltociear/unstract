import logging
import os
from abc import ABC, abstractmethod
from typing import Any

from fsspec import AbstractFileSystem

from unstract.connectors.base import UnstractConnector
from unstract.connectors.enums import ConnectorMode


class UnstractFileSystem(UnstractConnector, ABC):
    """Abstract class for file systems."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    )

    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    @staticmethod
    def get_id() -> str:
        return ""

    @staticmethod
    def get_name() -> str:
        return ""

    @staticmethod
    def get_description() -> str:
        return ""

    @staticmethod
    def get_icon() -> str:
        return ""

    @staticmethod
    def get_json_schema() -> str:
        return ""

    @staticmethod
    def can_write() -> bool:
        return False

    @staticmethod
    def can_read() -> bool:
        return False

    @staticmethod
    @abstractmethod
    def requires_oauth() -> bool:
        return False

    @staticmethod
    @abstractmethod
    def python_social_auth_backend() -> str:
        return ""

    @staticmethod
    def get_connector_mode() -> ConnectorMode:
        return ConnectorMode.FILE_SYSTEM

    @abstractmethod
    def get_fsspec_fs(self) -> AbstractFileSystem:
        pass

    @abstractmethod
    def test_credentials(self) -> bool:
        """Override to test credentials for a connector."""
        pass

    @staticmethod
    def get_connector_root_dir(input_dir: str, **kwargs: Any) -> str:
        """Override to get root dir of a connector."""
        return f"{input_dir.strip('/')}/"

    def create_dir_if_not_exists(self, input_dir: str) -> None:
        """Override to create dir of a connector if not exists."""
        fs_fsspec = self.get_fsspec_fs()
        try:
            is_dir = fs_fsspec.isdir(input_dir)
            print("*** current_dir ** ", dir)
            if not is_dir:
                fs_fsspec.mkdir(input_dir)
                print("*** dir created ** ")
        except Exception as e:
            print("*** exception type *** ", type(e))
            print("*** exception value *** ", str(e))

    def upload_file_to_storage(self, source_path: str, destination_path: str) -> None:
        normalized_path = os.path.normpath(destination_path)
        fs = self.get_fsspec_fs()
        try:
            with open(source_path, "rb") as source_file:
                fs.write_bytes(normalized_path, source_file.read())
        except Exception as e:
            print("*** exception type 1 *** ", type(e))
            print("*** exception value 1 *** ", str(e))
