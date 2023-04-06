from typing import Optional
import zipfile
from bcml.core.io import path, data


class Zip:
    def __init__(self, file_data: Optional["data.Data"] = None):
        mode = "r"
        if file_data is None:
            file_data = data.Data()
        if file_data.is_empty():
            mode = "w"
        self.file_data = file_data.to_bytes_io()
        self.zip = zipfile.ZipFile(
            self.file_data, mode=mode, compression=zipfile.ZIP_DEFLATED
        )

    @staticmethod
    def from_file(path: "path.Path") -> "Zip":
        return Zip(path.read())

    def add_file(self, file_name: "path.Path", file_data: "data.Data"):
        self.zip.writestr(file_name.to_str_forwards(), file_data.to_bytes())

    def get_file(
        self, file_name: "path.Path", show_error: bool = False
    ) -> Optional["data.Data"]:
        try:
            return data.Data(self.zip.read(file_name.to_str_forwards()))
        except KeyError:
            if show_error:
                print(f"File {file_name} not found in zip")
            return None

    def to_data(self) -> "data.Data":
        self.close()
        return data.Data(self.file_data.getvalue())

    def folder_exists(self, folder_name: str) -> bool:
        return folder_name in self.zip.namelist()

    def close(self):
        self.zip.close()

    def save(self, path: "path.Path"):
        self.close()
        path.write(self.to_data())

    def extract(self, path: "path.Path"):
        self.zip.extractall(path.to_str_forwards())
