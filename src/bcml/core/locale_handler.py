from bcml.core import io


class PropertySet:
    def __init__(self, locale: str, property: str):
        self.locale = locale
        self.path = (
            io.path.Path("locales", True).add(locale).add(property + ".properties")
        )
        self.properties: dict[str, str] = {}
        self.parse()

    def parse(self):
        lines = self.path.read().to_str().splitlines()
        for line in lines:
            if line.startswith("#") or line == "":
                continue
            key, value = line.split("=")
            self.properties[key] = value

    def get_key(self, key: str) -> str:
        return self.properties[key].replace("\\n", "\n")

    @staticmethod
    def from_config(property: str) -> "PropertySet":
        return PropertySet(io.config.Config().get(io.config.Key.LOCALE), property)


class LocalManager:
    def __init__(self, locale: str):
        self.locale = locale
        self.path = io.path.Path("locales", True).add(locale)
        self.properties: dict[str, PropertySet] = {}
        self.parse()

    def parse(self):
        for file in self.path.get_files():
            file_name = file.basename()
            if file_name.endswith(".properties"):
                self.properties[file_name[:-11]] = PropertySet(
                    self.locale, file_name[:-11]
                )

    def get_key(self, property: str, key: str) -> str:
        return self.properties[property].get_key(key)

    @staticmethod
    def from_config() -> "LocalManager":
        return LocalManager(io.config.Config().get(io.config.Key.LOCALE))
