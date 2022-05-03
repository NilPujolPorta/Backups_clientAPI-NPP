from datetime import datetime, timezone

#Retorna el temps actual en utc timestamp
def temps()-> int:
	dt = datetime.now(timezone.utc)
	utc_time = dt.replace(tzinfo=timezone.utc)
	utc_timestamp = utc_time.timestamp()
	return(round(utc_timestamp))

def utcToTime(utc_time:int)-> datetime:
	return datetime.utcfromtimestamp(utc_time)

def statusConvertor(status:int)->str:
	if status == 2:
		return("Correcte")
	elif status == 4:
		return("Warning")
	elif status == 5:
		return("Error")
	else:
		return("CodiDesconegut")
def statusConvertorPandora(status:int)->str:
	if status == 0:
		return("Correcte")
	elif status == 2:
		return("Warning")
	elif status == 200:
		return("Error")
	elif status == 100:
		return("Error")
	elif status == 3:
		return("Desconegut/desconectat")
	else:
		return("codi desconegut")