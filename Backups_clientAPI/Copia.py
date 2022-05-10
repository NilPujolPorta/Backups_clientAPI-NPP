import datetime


class Copia:
    def __init__(self, ID:str, Status:str, Data:datetime, LlocDeCopies):
        """Constructor of the Copia class 

        Parameters
        ----------
        ID : String
            The Copia ID or name(usually the former)

        Status : String
            The status of the backup operation

        Data : datetime
            the date of the backup operation

        LlocDeCopies : LlocDeCopies
            The platform where the backup operation was performed

        Returns
        -------
        Copia
            The newly instantiated Copia

        """
        self._ID = ID
        self._Status = Status
        self._Data = Data
        self._LlocDeCopies = LlocDeCopies

    def __str__(self) -> str:
        return "Nom: " + self._ID + " | Status: " + self._Status + " | Data: "+ str(self._Data) + " | Lloc de copies: " + self._LlocDeCopies.get_name()

    def get_status(self) -> str:
        """Returns the status of the backup operation"""
        return self._Status

    def get_data(self) -> datetime:
        """Returns the date of the backup operation"""
        return self._Data

    def get_id(self) -> int:
        """Returns the id of the backup operation"""
        return self._ID

    def get_LlocDeCopies(self):
        """Returns the LlocDeCopies of the backup operation"""
        return self._LlocDeCopies