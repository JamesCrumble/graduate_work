from enum import Enum


class UserHistoryOperation(Enum):
    SIGN: str = 'SIGN'
    LOGIN: str = 'LOGIN'
    LOGOUT: str = 'LOGOUT'
    CHANGE_PASSWORD: str = 'CHANGE_PASSWORD'
