import uvicorn
from fastapi import FastAPI
from data.package_repo import PackageRepo

# Constants

FAST_API_HOST = "localhost"
FAST_API_PORT = 8000

# Globals

app = FastAPI()


# Routes


@app.post("/add/{package_id}/{destination}")
def add(package_id: str, destination: str):
    PackageRepo.add(package_id, destination)
    return {"message": "OK"}


@app.get("/get/{package_id}")
def get(package_id: str):
    destination = PackageRepo.get(package_id)
    return {"destination": destination}

# Main

if __name__ == "__main__":
    uvicorn.run(app, host=FAST_API_HOST, port=FAST_API_PORT)
