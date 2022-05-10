from argparse import Namespace
import datetime
from importlib_metadata import List
import requests
from Copia import Copia
from utils import temps


class LlocDeCopies:
    #Constructor
    def __init__(self, name:str, url:str, user:str, password:str):
        """Constructor of the LlocDeCopies class 

        Parameters
        ----------
        name : String
            The object name

        url : String
            The url to the LlocDeCopies platform.

        user : String
            The user to use for the LlocDeCopies

        password : String
            The password to use for the LlocDeCopies

        Returns
        -------
        LlocDeCopies
            The newly instantiated LlocDeCopies object

        """
        self._name = name
        self._url = url
        self._user = user
        self._password = password
        self._copies = []
        self._tempsUltimCheck = temps() -2592000
    
    def __str__(self) -> str:
        return "Nom: " + self._name + " | Online: " + str(self.checkConnection()) + " | Tipus de copies: " + type(self).__name__

    def __repr__(self) -> str:
        return self._name

    #Getters i setters
    def set_tempsUltimCheck(self)->None:
        """Changes the tempsUltimCheck to the current time minus one month."""
        self._tempsUltimCheck = temps() - 2592000

    def get_tempsUltimCheck(self)->int:
        """Returns the last time it checked for copies"""
        return self._tempsUltimCheck

    def get_name(self) -> str:
        """Returns the name of the backup platform"""
        return self._name

    def get_user(self) -> str:
        """Returns the user of the backup platform"""
        return self._user

    def get_password(self) -> str:
        """Returns the password of the backup platform"""
        return self._password

    def get_url(self) -> str:
        """Returns the URL of the backup platform"""
        return self._url
        
    def get_num_copies(self) -> int:
        """Returns the number of the backup platform"""
        return len(self._copies)

    def get_copies(self)-> List[Copia]:
        """Returns the list of Copies of the backup platform"""
        return self._copies

############ Stop setters i getters normals

    def add_copies(self, new_copia:Copia) -> bool:
        """Add a given backup to the list of copies.
        
        Parameters
        ----------
        new_copia:Copia
            The backup to add.

        Returns
        -------
        Boolean
            If the backup is type Copia and the backup is not already in the list,True, otherwise False.

        """
        if (type(new_copia) == Copia and not(new_copia in self._copies)):
            self._copies.append(new_copia)
            return True
        return False

    def get_status_copies(self)-> List[str]:
        """
        Gets the status of all the copies
        
        Returns:
        -------
        List[str]
            List of all the status
        """
        ArrayStatus = []
        for copia in self._copies:
            ArrayStatus.append(copia.get_status())
        return ArrayStatus



    def checkConnection(self) -> bool:
        """
        Check if it is racheable
        
        Returns
        -------
        bool
            True if it's reachable, otherwise False.
        """
        try:
            requests.get(self._url)
        except:
            return False
        return True

    def retrieve_copies(self, ruta:str, args:Namespace)->None:
        """Saves copies to the array of this object
        
        Parameters
        ----------
        ruta : String
            Route to the folder the program is in.
        args:Namespace
            arguments of argsparse.
        """
        self.add_copies(Copia(self.get_name(), "Error en connectar amb la maquina", datetime.datetime.now(), self))
        return

