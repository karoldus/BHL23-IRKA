import uvicorn
from fastapi import FastAPI
from data.fake_package_repo import FakePackageRepo
from schemas.package_schema import PackageSchema
from model.package import Package

# Constants

FAST_API_HOST = "localhost"
FAST_API_PORT = 8000

# Globals

app = FastAPI()


# Routes


@app.post("/add_package")
def add_package(package: PackageSchema):
    FakePackageRepo.add_package(Package.from_package_schema(package))
    return {"message": "OK"}


@app.post("/add/{package_id}/{destination}")
def add_destination(package_id: str, destination: str):
    FakePackageRepo.set_destination(package_id, destination)
    return {"message": "OK"}


@app.get("/get/{package_id}")
def get_destination(package_id: str):
    destination = FakePackageRepo.get_destination(package_id)
    return {"destination": destination}


# Main

if __name__ == "__main__":
    uvicorn.run(app, host=FAST_API_HOST, port=FAST_API_PORT)
