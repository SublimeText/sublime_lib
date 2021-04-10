import shutil
from ..resource_path import ResourcePath


__all__ = ['TemporaryPackage']


class TemporaryPackage:
    def __init__(self, package_name: str, resource_path: ResourcePath) -> None:
        self.package_name = package_name
        self.resource_path = resource_path

    @property
    def package_path(self) -> ResourcePath:
        return ResourcePath("Packages") / self.package_name

    def create(self) -> None:
        shutil.copytree(
            src=str(self.resource_path.file_path()),
            dst=str(self.package_path.file_path()),
        )

    def destroy(self) -> None:
        shutil.rmtree(
            str(self.package_path.file_path()),
            ignore_errors=True
        )

    def exists(self) -> bool:
        return len(self.package_path.rglob('*')) > 0
