class PackageRepo:
    packages_destinations = {}

    @staticmethod
    def get(package_id):
        return PackageRepo.packages_destinations.get(package_id)

    @staticmethod
    def add(package_id, destination):
        PackageRepo.packages_destinations[package_id] = destination
