"""Handles locale files."""
from tbcml import core


class PropertySet:
    """Represents a set of properties in a property file."""

    def __init__(self, locale: str, property: str):
        """Initializes a new instance of the PropertySet class.

        Args:
            locale (str): Language code of the locale.
            property (str): Name of the property file.
        """
        self.locale = locale
        self.path = core.Path("locales", True).add(locale).add(property + ".properties")
        self.properties: dict[str, str] = {}
        self.parse()

    def parse(self):
        """Parses the property file.

        Raises:
            KeyError: If a key is already defined in the property file.
        """
        lines = self.path.read().to_str().splitlines()
        for line in lines:
            if line.startswith("#") or line == "":
                continue
            parts = line.split("=")
            if len(parts) < 2:
                continue
            key = parts[0]
            value = "=".join(parts[1:])
            if key in self.properties:
                raise KeyError(f"Key {key} already exists in property file")
            self.properties[key] = value

    def get_key(self, key: str) -> str:
        """Gets a key from the property file.

        Args:
            key (str): Key to get.

        Returns:
            str: Value of the key.
        """
        return self.properties[key].replace("\\n", "\n")

    @staticmethod
    def from_config(property: str) -> "PropertySet":
        """Gets a PropertySet from the language code in the config.

        Args:
            property (str): Name of the property file.

        Returns:
            PropertySet: PropertySet for the property file.
        """
        return PropertySet(core.Config().get(core.ConfigKey.LOCALE), property)


class LocalManager:
    """Manages properties for a locale"""

    def __init__(self, locale: str):
        """Initializes a new instance of the LocalManager class.

        Args:
            locale (str): Language code of the locale.
        """
        self.locale = locale
        self.path = core.Path("locales", True).add(locale)
        self.properties: dict[str, PropertySet] = {}
        self.all_properties: dict[str, str] = {}
        self.parse()

    def parse(self):
        """Parses all property files in the locale folder."""
        for file in self.path.get_files():
            file_name = file.basename()
            if file_name.endswith(".properties"):
                property_set = PropertySet(self.locale, file_name[:-11])
                self.all_properties.update(property_set.properties)
                self.properties[file_name[:-11]] = property_set

    def get_key(self, key: str) -> str:
        """Gets a key from the property file.

        Args:
            key (str): Key to get.

        Returns:
            str: Value of the key.
        """
        return self.all_properties[key]

    @staticmethod
    def from_config() -> "LocalManager":
        """Gets a LocalManager from the language code in the config.

        Returns:
            LocalManager: LocalManager for the locale.
        """
        return LocalManager(core.Config().get(core.ConfigKey.LOCALE))

    def check_duplicates(self):
        """Checks for duplicate keys in all property files.

        Raises:
            KeyError: If a key is already defined in the property file.
        """
        keys: set[str] = set()
        for property in self.properties.values():
            for key in property.properties.keys():
                if key in keys:
                    raise KeyError(f"Duplicate key {key}")
                keys.add(key)
