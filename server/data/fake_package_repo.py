from typing import Dict, List
from model.package import Package
from .package_repo import PackageRepo

class FakePackageRepo(PackageRepo):
    packages = list()
    # packages_destinations = Dict[str, str]

    @staticmethod
    def add_package(package: Package):
        FakePackageRepo.packages.append(package)

    @staticmethod
    def get_packages() -> List[Package]:
        return FakePackageRepo.packages
    
    @staticmethod
    def get_package_details(package_id: str) -> Package:
        for package in FakePackageRepo.packages:
            if package.id == package_id:
                return package
        return None
    
    @staticmethod
    def get_package_destination(package_id: str) -> str:
        for package in FakePackageRepo.packages:
            if package.id == package_id:
                return package.destination
        return None
    
    @staticmethod
    def get_packages_in_destination(destination: int) -> List[Package]:
        packages = list()
        for package in FakePackageRepo.packages:
            if package.destination == destination:
                packages.append(package)
        return packages