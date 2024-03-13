# demo-azurite

A sample project put together to demo emulating Azure Storage for local development in Python.

# # Prerequisites
- Azurite service running with Blob port exposed

# # Setup
- Create a virtual environment
- From root directory of the project, run: pip install requirements.txt

# # How to run the API
- From root directory of the project, run: uvicorn app.main:app --reload

# # How to run tests
- From root directory of the project, run: pytest