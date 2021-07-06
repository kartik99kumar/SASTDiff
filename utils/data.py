import json
config = open("config.json", "r")
data = json.load(config)

validationFunctions = data["validationFunctions"]
allowedAddresses = data["allowedAddresses"]
