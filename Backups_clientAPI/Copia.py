from datetime import date


#amb copies hi han dos opcions, o guardem nomes les ultimes en un json i per mirar antigues a el nas en si o
#les guardem totes(fins a un limit) en una base de dades

class Copia:
    def __init__(self, ID:int, Status:str, Data:date, LlocDeCopies):

        self._ID = ID
        self._Status = Status
        self._Data = Data
        self._LlocDeCopies = LlocDeCopies

    def get_status(self) -> str:
        return self._Status

    def get_data(self) -> date:
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