from database import get_list

class DeviceList:
	def __init__(self):
		_list = get_list()
		index = 0
		self.choices = []
		self.devices = {}
		for name, ip in _list:
			key_value = 'dev' + str(index)
			self.choices.append((key_value, name))
			self.devices[key_value] = { 'name' : name, 'ip' : ip }
			index += 1
	def __getitem__(self, key_value):
		return self.devices[key_value]
