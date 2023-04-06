import enum


class CountryCode(enum.Enum):
    EN = "en"
    JP = "jp"
    KR = "kr"
    TW = "tw"

    def get_code(self) -> str:
        return self.value

    def get_patching_code(self) -> str:
        return self.get_code().replace("jp", "")

    @staticmethod
    def from_patching_code(code: str) -> "CountryCode":
        if code == "":
            return CountryCode.JP
        return CountryCode.from_code(code)

    @staticmethod
    def from_code(code: str) -> "CountryCode":
        code = code.lower()
        for country_code in CountryCode:
            if country_code.get_code() == code:
                return country_code
        return CountryCode.EN

    @staticmethod
    def get_all() -> list["CountryCode"]:
        return list(CountryCode)

    @staticmethod
    def get_all_str() -> list[str]:
        return [country_code.get_code() for country_code in CountryCode.get_all()]

    def __str__(self) -> str:
        return self.get_code()

    def __repr__(self) -> str:
        return f"CountryCode.{self.name}"

    def copy(self) -> "CountryCode":
        return self
