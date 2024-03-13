# demo-azurite
A sample project put together to demo emulating Azure Storage for local development in Python.

### Requirements
- Azurite service running with Blob port exposed https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=docker-hub%2Cblob-storage
- Microsoft Azure Storage Explorer https://azure.microsoft.com/en-gb/products/storage/storage-explorer

### Setup
- Create a virtual environment
- From root directory of the project, run: `pip install requirements.txt`

### How to run the API
- From root directory of the project, run: `uvicorn app.main:app --reload`

### How to run tests
- From root directory of the project, run: `pytest`
(In case of import errors, try setting the PYTHONPATH variable to project root directory prior to invoking pytest: `PYTHONPATH=$PWD pytest`)