import datetime
import utils
import requests
from LlocDeCopies import LlocDeCopies
from Copia import Copia

class Pandora(LlocDeCopies):
    def __init__(self, name:str, url:str, user:str, password:str, apipassw:str):
        self._apipassw = apipassw
        super().__init__(name, url, user, password)
    
    def retrieve_copies(self, ruta:str, args) -> None:
        metode = "all_agents"
        other = ";|%20|type_row,group_id,agent_name"
        other2 = "url_encode_separator_|"
        try:
            parameters = {"op":"get", "op2":metode, "return_type":"json", "apipass":self._apipassw, "user":super().get_user(), "pass":super().get_password()}
            agentsFull = requests.get(super().get_url(), params=parameters).json()
        except Exception as e:
            print("Error de conexio")
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-Connexio')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write("Error de conexio"+str(e))
            f.close()
            return

        for agent in agentsFull['data']:
            super().add_copies(Copia(agent['alias'], utils.statusConvertorPandora(agent['status']), datetime.datetime.now(), self))