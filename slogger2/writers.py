class BaseWriter(object):
	def __init__(self, dayone_entry):
		self.dayone_entry = dayone_entry

	def generate(self):
		raise NotImplemented("You must implament `generate` within your writer class")

class XMLWriter(BaseWriter):

        top = """\                                                                                                                                                                
<?xml version="1.0" encoding="UTF-8"?>                                                                                                                                            
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">"""
        pass
