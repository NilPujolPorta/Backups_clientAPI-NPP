import datetime


class Copia:
    def __init__(self, ID:str, Status:str, Data:datetime, LlocDeCopies):

        self._ID = ID
        self._Status = Status
        self._Data = Data
        self._LlocDeCopies = LlocDeCopies

    def __str__(self) -> str:
        return "Nom: " + self._ID + " | Status: " + self._Status + " | Data: "+ str(self._Data) + " | Lloc de copies: " + self._LlocDeCopies.get_name()

    def get_status(self) -> str:
        return self._Status

    def get_data(self) -> datetime:
        return self._Data

    def get_id(self) -> int:
        return self._ID

    def get_LlocDeCopies(self):
        return self._LlocDeCopies

    def set_llocDeCopies(self, llocDeCopies)->bool:
        from LlocDeCopies import LlocDeCopies
        if (type(llocDeCopies)==LlocDeCopies):
            self._LlocDeCopies = llocDeCopies
            return True
        return False