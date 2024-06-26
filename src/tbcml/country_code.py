"""Country code enum."""

from __future__ import annotations

import enum
from typing import Literal
import tbcml


class CountryCode(enum.Enum):
    """Country code enum."""

    EN = "en"
    JP = "jp"
    KR = "kr"
    TW = "tw"

    @staticmethod
    def from_cc(cc: tbcml.CC):
        if isinstance(cc, str):
            return CountryCode.from_code(cc)
        return cc

    def get_code(self) -> str:
        """Gets the 2 letter lowercase country code.

        Returns:
            str: The 2 letter lowercase country code.
        """
        return self.value

    def get_patching_code(self) -> str:
        """Gets the 2 letter lowercase country code, jp is an empty string.

        Returns:
            str: The 2 letter lowercase country code, jp is an empty string.
        """
        return self.get_code().replace("jp", "")

    def get_request_code(self) -> str:
        """Gets the 2 letter lowercase country code, jp is ja

        Returns:
            str: The 2 letter lowercase country code, jp is ja
        """
        return self.get_code().replace("jp", "ja")

    @staticmethod
    def from_patching_code(code: str) -> CountryCode:
        """Gets the country code from the patching code.

        Args:
            code (str): The patching code. jp is an empty string.

        Returns:
            CountryCode: The country code.
        """
        if code == "":
            return CountryCode.JP
        return CountryCode.from_code(code)

    @staticmethod
    def from_code(code: str) -> CountryCode:
        """Gets the country code from the 2 letter lowercase country code.

        Args:
            code (str): The 2 letter lowercase country code.

        Returns:
            CountryCode: The country code.
        """
        code = code.lower()
        for country_code in CountryCode:
            if country_code.get_code() == code:
                return country_code
        return CountryCode.JP

    @staticmethod
    def get_all() -> list[CountryCode]:
        """Gets all country codes.

        Returns:
            list[CountryCode]: All country codes.
        """
        return list(CountryCode)

    @staticmethod
    def get_all_str() -> list[str]:
        """Gets all country codes as strings.

        Returns:
            list[str]: All country codes as strings.
        """
        return [country_code.get_code() for country_code in CountryCode.get_all()]

    def index(self) -> int:
        """Gets the index of the country code.

        Returns:
            int: The index of the country code.
        """
        return CountryCode.get_all().index(self)

    def __str__(self) -> str:
        """Gets the 2 letter lowercase country code.

        Returns:
            str: The 2 letter lowercase country code.
        """
        return self.get_code()

    def __repr__(self) -> str:
        """Gets the 2 letter lowercase country code.

        Returns:
            str: The 2 letter lowercase country code.
        """
        return f"CountryCode.{self.name}"

    @staticmethod
    def from_package_name(package_name: str) -> CountryCode:
        """Gets the country code from the package name.

        Args:
            package_name (str): The package name.

        Returns:
            CountryCode: The country code.
        """
        for country_code in CountryCode:
            if package_name.endswith(country_code.get_code()):
                return country_code
        return CountryCode.JP

    def get_language(self) -> str:
        """Gets the language code.

        Returns:
            str: The language code.
        """
        if self == CountryCode.EN:
            return "en"
        if self == CountryCode.JP:
            return "ja"
        if self == CountryCode.KR:
            return "ko"
        if self == CountryCode.TW:
            return "tw"

        return "en"


CC = Literal["en"] | Literal["jp"] | Literal["kr"] | Literal["tw"] | CountryCode
