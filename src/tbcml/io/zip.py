from __future__ import annotations

import zipfile
import tbcml


class Zip:
    password_length = 16

    def __init__(
        self,
        file_data: tbcml.Data | None = None,
        compression: int = zipfile.ZIP_DEFLATED,
    ):
        mode = "r"
        if file_data is None:
            file_data = tbcml.Data()
        if file_data.is_empty():
            mode = "w"
        self.file_data = file_data.to_bytes_io()

        self.zip = zipfile.ZipFile(self.file_data, mode=mode, compression=compression)

    @staticmethod
    def compress_directory(
        directory_path: tbcml.Path,
        output_path: tbcml.Path,
        compression: int = zipfile.ZIP_DEFLATED,
        extensions_to_store: list[str] | None = None,
    ):
        with zipfile.ZipFile(output_path.to_str_forwards(), "w", compression) as zipf:
            for file in directory_path.get_files_recursive():
                cmp = compression
                if extensions_to_store is not None:
                    if file.get_extension() in extensions_to_store:
                        cmp = zipfile.ZIP_STORED

                zipf.write(
                    file.to_str_forwards(),
                    file.replace(directory_path.to_str(), "").to_str_forwards(),
                    compress_type=cmp,
                )

    @staticmethod
    def from_file(path: tbcml.Path) -> Zip:
        return Zip(path.read())

    def add_file(self, file_name: tbcml.Path, file_data: tbcml.Data):
        self.zip.writestr(file_name.to_str_forwards(), file_data.to_bytes())

    def get_file(
        self, file_name: tbcml.Path, show_error: bool = False
    ) -> tbcml.Data | None:
        try:
            return tbcml.Data(self.zip.read(file_name.to_str_forwards()))
        except KeyError:
            if show_error:
                print(f"File {file_name} not found in zip")
            return None

    def to_data(self) -> tbcml.Data:
        self.close()
        data = tbcml.Data(self.file_data.getvalue())
        return data

    def folder_exists(self, folder_name: str) -> bool:
        return folder_name in self.zip.namelist()

    def close(self):
        self.zip.close()

    def save(self, path: tbcml.Path):
        self.close()
        path.write(self.to_data())

    def extract(self, path: tbcml.Path):
        self.zip.extractall(path.to_str_forwards())

    def get_paths(self) -> list[tbcml.Path]:
        return [tbcml.Path(name) for name in self.zip.namelist()]

    def get_paths_in_folder(self, folder_name: tbcml.Path) -> list[tbcml.Path]:
        return [
            tbcml.Path(name)
            for name in self.zip.namelist()
            if name.startswith(folder_name.to_str_forwards())
        ]
