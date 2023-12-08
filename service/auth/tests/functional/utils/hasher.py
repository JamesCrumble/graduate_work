import abc
import hashlib
import os


class BaseHasher(abc.ABC):
    @abc.abstractmethod
    def encode(self, password: str) -> str:
        pass

    @abc.abstractmethod
    def check(self, password: str, has: str) -> bool:
        pass


class PBKDHasher(BaseHasher):

    def encode(self, password: str) -> str:
        salt = os.urandom(32).hex()
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return salt + key.hex()

    def check(self, password: str, password_hash: str) -> bool:
        salt = password_hash[:64]
        key_hash = password_hash[64:]
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return key == key_hash


if __name__ == '__main__':

    val = PBKDHasher().encode('password')
