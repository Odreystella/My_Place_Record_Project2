from dataclasses import dataclass

@dataclass
class ValidTokenDto():
    pk = int
    token = str
    