from datetime import datetime, timezone

def temps()-> int:
	"""Gives the time in utc timestamp

	Returns
	-------
	int
	  Current time in utc timestamp.

	"""
	dt = datetime.now(timezone.utc)
	utc_time = dt.replace(tzinfo=timezone.utc)
	utc_timestamp = utc_time.timestamp()
	return(round(utc_timestamp))

def utcToTime(utc_time:int)-> datetime:
	"""Gives datetime of a given utc timestamp.
	
	Parameters
	----------
	utc_time:int
		A certain time in utc timestamp

	Returns
	-------
	datetime
		datetime of the given utc timestamp.

	"""
	return datetime.utcfromtimestamp(utc_time)

def statusConvertor(status:int)->str:
	"""Gives the status of a status code from the synology api.
	
	Parameters
	----------
	status:int
		the status code to convert

	Returns
	-------
	String
		The status code conveted to the status name.

	"""
	if status == 2:
		return("Correcte")
	elif status == 4:
		return("Warning")
	elif status == 5:
		return("Error")
	else:
		return("CodiDesconegut")
def statusConvertorPandora(status:int)->str:
	"""Gives the status of a status code from the PandoraFMS api.
	
	Parameters
	----------
	status:int
		the status code to convert

	Returns
	-------
	String
		The status code conveted to the status name.

	"""
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