from abc import ABC, abstractmethod
from model.package import Package


class PackageRepo(ABC):
    @abstractmethod
    def add_package(package: Package):
        pass

    @abstractmethod
    def get_destination(package_id: str):
        pass

    @abstractmethod
    def set_destination(package_id: str, destination: str):
        pass
