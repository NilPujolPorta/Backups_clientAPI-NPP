from datetime import datetime, timezone

#Retorna el temps actual en utc timestamp
def temps():
	dt = datetime.now(timezone.utc)
	utc_time = dt.replace(tzinfo=timezone.utc)
	utc_timestamp = utc_time.timestamp()
	return(round(utc_timestamp))

def statusConvertor(status):
	if status == 2:
		return("Correcte")
	elif status == 4:
		return("Warning")
	elif status == 5:
		return("ERROR")
	else:
		return("codi desconegut")