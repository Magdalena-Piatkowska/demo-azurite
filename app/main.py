from io import StringIO
from fastapi import Depends, FastAPI, HTTPException
from azure.storage.blob import BlobServiceClient, BlobClient
from app.config import AZURE_STORAGE_CONNECTION_STRING, CONTAINER_NAME


class BlobException(Exception):
     pass


def get_container_name():
    return CONTAINER_NAME


def get_blob_service_client():
    client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING
        )
    yield client


def get_container(container_name=get_container_name(), blob_service_client=get_blob_service_client):
    try:
        blob_service_client.create_container(container_name)
    except:
        pass
    return container_name

     
def load(file_path, blob_service_client, container_name) -> StringIO:
        try:
            blob_client: BlobClient = blob_service_client.get_blob_client(
                container=container_name, blob=file_path
            )
            return StringIO(blob_client.download_blob().readall().decode("utf-8"))
        except Exception as err:
            raise BlobException(
                f"File not found, container: {container_name}. path: {file_path}"
            )


app = FastAPI()

@app.get("/api/file-content")
def get_file(
    blob_service_client = Depends(get_blob_service_client),
    container_name = Depends(get_container_name),
    container = Depends(get_container),
    ):
    try:
        file_content = load(file_path="demo_preparation.txt", blob_service_client=blob_service_client, container_name=container)
        return {"message": f"{str(file_content.getvalue())}"}
    
    except BlobException as err:
        raise HTTPException(status_code=404, detail=str(err))