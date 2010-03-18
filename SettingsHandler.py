#!/usr/bin/python
import xml.dom.minidom
import sys
from xml.dom.minidom import Node
 
class SettingsHandler():
	def __init__(self):
		self.load_settings()		

	def load_settings(self):
		try:
			self.doc = xml.dom.minidom.parse("settings.xml")
		except Exception:
			print "Error reading config file"
			sys.exit()

	def get_accounts(self):
		accounts_dict = list()
		accounts = self.doc.getElementsByTagName("account")
		for account in accounts:
			accounts_dict.append([account.getAttribute("login"),
                            account.getAttribute("password"),
                            account.getAttribute("default")])
		return accounts_dict

	def print_xml(self):
		print self.doc.toxml("UTF-8")


#settings = SettingsHandler()
#print settings.get_accounts()

#another = doc.createElement("account")
#another.setAttribute("login", "maria")
#accounts.item(0).appendChild(another)


#for dom1 in doc.getElementsByTagName("accounts"):
#	login = dom1.getAttribute("login")
#	password = dom1.getAttribute("password")
#	default = dom1.getAttribute("default")

