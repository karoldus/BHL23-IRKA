from typing import Dict, List
from model.package import Package
from .package_repo import PackageRepo

class FakePackageRepo(PackageRepo):
    packages = List[Package]
    packages_destinations = Dict[str, str]

    @staticmethod
    def add_package(package: Package):
        FakePackageRepo.packages.append(package)

    @staticmethod
    def get_destination(package_id):
        return FakePackageRepo.packages_destinations.get(package_id)

    @staticmethod
    def set_destination(package_id, destination):
        FakePackageRepo.packages_destinations[package_id] = destination
