from importlib_metadata import List
import requests
from Copia import Copia
from utils import temps


class LlocDeCopies:
    #Constructor
    def __init__(self, name:str, url:str, user:str, password:str):
        self._name = name
        self._url = url
        self._user = user
        self._password = password
        self._tamanyTotalGB = -1
        self._tamanyLliureGB = -1
        self._tamanyOcupatGB = -1
        self._copies = []
        self._tempsUltimCheck = temps() -2592000
    
    def __str__(self) -> str:
        return "Nom: " + self._name + " | Online: " + str(self.checkConnection()) + " | Tipus de copies: " + type(self).__name__

    def __repr__(self) -> str:
        return self._name

    #Getters i setters
    def set_tempsUltimCheck(self)->None:
        self._tempsUltimCheck = temps() - 2592000

    def get_tempsUltimCheck(self)->int:
        return self._tempsUltimCheck

    def get_name(self) -> str:
        return self._name

    def get_user(self) -> str:
        return self._user

    def get_password(self) -> str:
        return self._password

    def get_url(self) -> str:
        return self._url

    def get_tamanyTotalGB(self) -> float:
        if(self._tamanyTotalGB == -1):
            return None
        return self._tamanyTotalGB
    
    def set_tamanyTotalGB(self, tamanyTotalGB:float)-> None:
        self._tamanyTotalGB = tamanyTotalGB
        if(self._tamanyTotalGB < 0):
            self._tamanyTotalGB = -1

    def get_tamanyLliureGB(self) -> float:
        if(self._tamanyLliureGB == -1):
            return None
        return self._tamanyLliureGB

    def set_tamanyLliureGB(self, tamanyLliureGB:float)-> None:
        self._tamanyLliureGB = tamanyLliureGB
        if(self._tamanyLliureGB < 0):
            self._tamanyLliureGB = -1

    def get_tamanyOcupatGB(self) -> float:
        if(self._tamanyOcupatGB == -1):
            return None
        return self._tamanyOcupatGB

    def set_tamanyOcupatGB(self, tamanyOcupatGB:float)-> None:
        self._tamanyOcupatGB = tamanyOcupatGB
        if(self._tamanyOcupatGB < 0):
            self._tamanyOcupatGB = -1

    def add_copies(self, new_copies:Copia) -> bool:
        if (type(new_copies) == Copia):
            self._copies.append(new_copies)
            return True
        return False
        
    def get_num_copies(self) -> int:
        return len(self._copies)

    def get_copies(self)-> List[Copia]:
        return self._copies

############ Stop setters i getters normals

    def checkConnection(self) -> bool:
        try:
            requests.get(self._url)
        except:
            return False
        return True

