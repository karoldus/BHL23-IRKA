import uvicorn
from fastapi import FastAPI
from data.fake_package_repo import FakePackageRepo
from schemas.package_schema import PackageSchema
from model.package import Package
from fastapi.middleware.cors import CORSMiddleware

# Constants

FAST_API_HOST = "localhost"
FAST_API_PORT = 8000

HEIGHT_LIMIT_1 = 7


# Globals

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes

@app.post("/package")
def create_package(package_id: str, height: float):

    if height < HEIGHT_LIMIT_1:
        destination = 1
    else:
        destination = 2
    
    package = Package(package_id, height, destination)
    FakePackageRepo.add_package(package)

    # FakePackageRepo.set_destination(package.id, destination)
    return {"destination": destination}

@app.get("/packages")
def get_packages():
    packages = FakePackageRepo.get_packages()
    return packages

@app.get("/package/{package_id}")
def get_package(package_id: str):
    package = FakePackageRepo.get_package_details(package_id)
    return package

@app.get("/packages/{destination}")
def get_packages_in_destination(destination: int):
    packages = FakePackageRepo.get_packages_in_destination(destination)
    return packages


# Main

if __name__ == "__main__":
    uvicorn.run(app, host=FAST_API_HOST, port=FAST_API_PORT)
