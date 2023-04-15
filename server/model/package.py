from schemas.package_schema import PackageSchema


class Package:
    def __init__(self, package_id, height) -> None:
        self.id = package_id
        self.height = height

    @classmethod
    def from_package_schema(cls, package_schema: PackageSchema):
        return cls(package_schema.package_id, package_schema.height)
