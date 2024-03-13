import os

from fastapi.testclient import TestClient
from azure.storage.blob import BlobServiceClient

import pytest
from unittest import mock

from app.config import AZURE_STORAGE_CONNECTION_STRING


@pytest.fixture
def mock_container_name():
    container_name = "demo-azurite-test"
    with mock.patch(
        "app.main.get_container_name",
    ) as mock_get_container_name:
        mock_get_container_name.return_value = container_name

        yield container_name


@pytest.fixture
def blob_service_client():
    client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING
        )
    yield client


@pytest.fixture
def mock_container(mock_container_name, blob_service_client):
    container_name = mock_container_name
    try:
        blob_service_client.delete_container(container_name)
    except:
        pass
    blob_service_client.create_container(container_name)

    return container_name


@pytest.fixture
def api_client(mock_container_name, mock_container):
    from app.main import app, get_container_name, get_container

    def get_container_name_override():
        yield mock_container_name

    def get_container_override():
        yield mock_container

    app.dependency_overrides[get_container_name] = get_container_name_override
    app.dependency_overrides[get_container] = get_container_override

    return TestClient(app)


@pytest.fixture
def load_file(blob_service_client, mock_container):
    ROOT_DIR = os.path.dirname(os.path.realpath("__file__"))

    file_path = f"demo_preparation.txt"
    test_file_path = os.path.join(ROOT_DIR, "tests/data/demo_preparation.txt")
    with open(test_file_path, "r") as file_pointer:
        contents = file_pointer.read()

    blob_client = blob_service_client.get_blob_client(
            container=mock_container, blob=file_path
        )
    blob_client.upload_blob(data=contents, overwrite=True)

    return file_path


def test_get_file_content(api_client, load_file):
    response = api_client.get("/api/file-content")
    assert response.status_code == 200
    assert response.json()["message"] == 'this is a test'
    


