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
                            account.getAttribute("default"),
                            account.getAttribute("pro")])
		return accounts_dict

	def add_account(self, login, password, default, pro):
		if self.account_exists(login):
			return False
		else:
			if default == "True" and self.account_default_exists():
				return False
			else:
				account = self.doc.createElement("account")
				account.setAttribute("login", login)
				account.setAttribute("password", password)
				account.setAttribute("default", default)
				account.setAttribute("pro", pro)
				accounts = self.doc.getElementsByTagName("accounts")
				accounts[0].appendChild(account)
				self.save_xml()
				return True

	def account_default_exists(self):
		accounts = self.doc.getElementsByTagName("account")
		for account in accounts:
			if account.getAttribute("default") == "True":
				return True
		return False

	def account_exists(self, login):
		accounts = self.doc.getElementsByTagName("account")
		for account in accounts:
			if account.getAttribute("login") == login:
				return True
		return False

	def remove_account(self, login):
		accounts = self.doc.getElementsByTagName("account")
		for account in accounts:
			if account.getAttribute("login") == login:
				account.parentNode.removeChild(account)
				break
		self.save_xml()

	def save_xml(self):
		#TODO: Remove empty lines in xml file
		filep = file("settings.xml", "w")
		self.doc.writexml(filep, "\t", "\t", "\n", "UTF-8")
		filep.close()
				
	def print_xml(self):
		print self.doc.toxml("UTF-8")
