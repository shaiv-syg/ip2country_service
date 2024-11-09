from abc import ABC, abstractmethod

class IP2CountryDatabase(ABC):
    @abstractmethod
    def lookup(self, ip_address: str) -> dict:
        pass 