from pydantic import BaseModel

class PackageSchema(BaseModel):
    package_id: str
    height: float
