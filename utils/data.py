import json
config = open("config.json", "r")
data = json.load(config)

validationFunctions = data["validationFunctions"]
allowedAddresses = data["allowedAddresses"]
logFile = open("logs/log.txt", "w")
stateFile = open("logs/state.txt", "w")
