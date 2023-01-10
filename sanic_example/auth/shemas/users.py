from dataclasses import dataclass

@dataclass
class UserCreate:
    first_name: str
    password: str
    role: str

@dataclass
class UserAuth:
    first_name: str
    password: str