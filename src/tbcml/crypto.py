"""A module for cryptography."""

from __future__ import annotations

import enum
import hashlib
import hmac
import random

from Cryptodome.Cipher import AES, _mode_cbc, _mode_ecb

import tbcml


class HashAlgorithm(enum.Enum):
    """An enum representing a hash algorithm."""

    MD5 = enum.auto()
    SHA1 = enum.auto()
    SHA256 = enum.auto()


class Hash:
    """A class to hash data."""

    def __init__(self, algorithm: HashAlgorithm):
        """Initializes a new instance of the Hash class.

        Args:
            algorithm (HashAlgorithm): The hash algorithm to use.
        """
        self.algorithm = algorithm

    def get_hash(
        self,
        data: tbcml.Data,
        length: int | None = None,
    ) -> tbcml.Data:
        """Gets the hash of the given data.

        Args:
            data (tbcml.Data): The data to hash.
            length (int | None, optional): The length of the hash. Defaults to None.

        Raises:
            ValueError: Invalid hash algorithm.

        Returns:
            tbcml.Data: The hash of the data.
        """
        if self.algorithm == HashAlgorithm.MD5:
            hash = hashlib.md5()
        elif self.algorithm == HashAlgorithm.SHA1:
            hash = hashlib.sha1()
        elif self.algorithm == HashAlgorithm.SHA256:
            hash = hashlib.sha256()
        else:
            raise ValueError("Invalid hash algorithm")
        hash.update(data.get_bytes())
        if length is None:
            return tbcml.Data(hash.digest())
        return tbcml.Data(hash.digest()[:length])


class AesCipher:
    """A class to represent an AES cipher."""

    def __init__(
        self,
        key: bytes,
        iv: bytes | None = None,
        mode: int | None = None,
        enable: bool = True,
    ):
        """Initializes a new instance of the AesCipher class.

        Args:
            key (bytes): Key to use.
            iv (bytes | None, optional): Initialization vector to use. Defaults to None.
            mode (int | None, optional): Mode to use. Defaults to None.
            enable (bool, optional): Whether to enable encryption. Defaults to True. ImageDataLocal is a pack that is not encrypted.
        """
        self.key = key
        self.iv = iv
        if mode is None:
            if iv is None:
                mode = AES.MODE_ECB
            else:
                mode = AES.MODE_CBC
        self.mode = mode
        self.enable = enable

    def get_cipher(self) -> _mode_ecb.EcbMode | _mode_cbc.CbcMode:
        """Gets the cipher.

        Returns:
            _mode_ecb.EcbMode | _mode_cbc.CbcMode: The cipher.
        """
        if self.iv is None:
            return AES.new(self.key, self.mode)  # type: ignore
        else:
            return AES.new(self.key, self.mode, self.iv)  # type: ignore

    def encrypt(self, data: tbcml.Data) -> tbcml.Data:
        """Encrypts the given data.

        Args:
            data (tbcml.Data): The data to encrypt.

        Returns:
            tbcml.Data: The encrypted data.
        """
        if not self.enable:
            return data
        cipher = self.get_cipher()
        return tbcml.Data(cipher.encrypt(data.get_bytes()))

    @staticmethod
    def get_key_length(has_iv: bool) -> int:
        if has_iv:
            return 16
        return 8

    def decrypt(self, data: tbcml.Data) -> tbcml.Data:
        """Decrypts the given data.

        Args:
            data (tbcml.Data): The data to decrypt.

        Returns:
            tbcml.Data: The decrypted data.
        """
        if not self.enable:
            return data
        cipher = self.get_cipher()
        return tbcml.Data(cipher.decrypt(data.get_bytes()))

    @staticmethod
    def get_key_iv_from_cc(cc: tbcml.CountryCode) -> tuple[str, str]:
        """Gets the key and iv from the country code.

        Args:
            cc (tbcml.CountryCode): The country code.

        Raises:
            ValueError: Unknown country code.

        Returns:
            tuple[str, str]: The key and iv.
        """
        if cc == tbcml.CountryCode.JP:
            key = "d754868de89d717fa9e7b06da45ae9e3"
            iv = "40b2131a9f388ad4e5002a98118f6128"
        elif cc == tbcml.CountryCode.EN:
            key = "0ad39e4aeaf55aa717feb1825edef521"
            iv = "d1d7e708091941d90cdf8aa5f30bb0c2"
        elif cc == tbcml.CountryCode.KR:
            key = "bea585eb993216ef4dcb88b625c3df98"
            iv = "9b13c2121d39f1353a125fed98696649"
        elif cc == tbcml.CountryCode.TW:
            key = "313d9858a7fb939def1d7d859629087d"
            iv = "0e3743eb53bf5944d1ae7e10c2e54bdf"
        else:
            raise ValueError("Unknown country code")
        return key, iv

    @staticmethod
    def get_cipher_from_pack(
        cc: tbcml.CountryCode,
        pack_name: str,
        gv: tbcml.GameVersion,
        force_server: bool = False,
        key: str | None = None,
        iv: str | None = None,
    ) -> "AesCipher":
        """Gets the cipher from the pack.

        Args:
            cc (country_code.CountryCode): The country code.
            pack_name (str): The pack name.
            gv (game_version.GameVersion): The game version.
            force_server (bool, optional): Whether to force the decryption to use the server key. Defaults to False.
            key (str | None, optional): The key to use. Defaults to None.
            iv (str | None, optional): The iv to use. Defaults to None.

        Raises:
            Exception: Unknown country code.

        Returns:
            AesCipher: The cipher.
        """
        aes_mode = AES.MODE_CBC
        key_, iv_ = AesCipher.get_key_iv_from_cc(cc)
        if key is None:
            key = key_
        if iv is None:
            iv = iv_
        enable = not tbcml.PackFile.is_image_data_local_pack(pack_name)
        if force_server:
            enable = True
        if (
            tbcml.PackFile.is_server_pack(pack_name)
            or gv < tbcml.GameVersion.from_string("8.9.0")
            or force_server
        ):
            aes_mode = AES.MODE_ECB
            key = Hash(HashAlgorithm.MD5).get_hash(tbcml.Data("battlecats"), 8).to_hex()
            return AesCipher(key.encode("utf-8"), None, aes_mode, enable)
        return AesCipher(bytes.fromhex(key), bytes.fromhex(iv), aes_mode, enable)


class Hmac:
    """A class to do HMAC stuff."""

    def __init__(self, key: tbcml.Data, algorithm: HashAlgorithm):
        """Initializes a new instance of the Hmac class.

        Args:
            key (tbcml.Data): Key to use.
            algorithm (HashAlgorithm): Algorithm to use.
        """
        self.key = key
        self.algorithm = algorithm

    def get_hmac(self, data: tbcml.Data) -> tbcml.Data:
        """Gets the HMAC of the given data.

        Args:
            data (tbcml.Data): The data to get the HMAC of.

        Raises:
            ValueError: Invalid hash algorithm.

        Returns:
            tbcml.Data: The HMAC.
        """
        if self.algorithm == HashAlgorithm.MD5:
            hash = hashlib.md5
        elif self.algorithm == HashAlgorithm.SHA1:
            hash = hashlib.sha1
        elif self.algorithm == HashAlgorithm.SHA256:
            hash = hashlib.sha256
        else:
            raise ValueError("Invalid hash algorithm")
        return tbcml.Data(
            hmac.new(self.key.to_bytes(), data.get_bytes(), hash).digest()
        )


class Random:
    """A class to get random data"""

    @staticmethod
    def get_bytes(length: int) -> bytes:
        """Gets random bytes.

        Args:
            length (int): The length of the bytes.

        Returns:
            bytes: The random bytes.
        """
        return bytes(random.getrandbits(8) for _ in range(length))

    @staticmethod
    def get_alpha_string(length: int) -> str:
        """Gets a random string of the given length.

        Args:
            length (int): The length of the string.

        Returns:
            str: The random string.
        """
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def get_hex_string(length: int) -> str:
        """Gets a random hex string of the given length.

        Args:
            length (int): The length of the string.

        Returns:
            str: The random string.
        """
        characters = "0123456789abcdef"
        return "".join(random.choice(characters) for _ in range(length))
