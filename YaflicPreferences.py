#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import gtk, gobject
import os
import pango
from SettingsHandler import *

class YaflicPreferences(object):
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("glade/yaflic-preferences.glade")
		self.window = self.builder.get_object("PreferencesDialog")
		self.categories = self.builder.get_object("IconViewPreferences")
		self.notebook = self.builder.get_object("notebook1")

		self.builder.connect_signals(self)

		model = gtk.ListStore(str, gtk.gdk.Pixbuf)
		pixbuf = gtk.gdk.pixbuf_new_from_file('images/prefs_general.png')
		model.append(['General', pixbuf])

		pixbuf = gtk.gdk.pixbuf_new_from_file('images/prefs_users.png')
		model.append(['Accounts', pixbuf])

		self.categories.set_item_width(94)

		self.categories.set_text_column(0)
		self.categories.set_pixbuf_column(1)

		self.categories.set_model(model)

		while gtk.events_pending():
			gtk.main_iteration()

		self.categories.select_path((0,))
	
		# Draw TreeView (Accounts List)
		self.treeview = self.builder.get_object("TreeViewAccountsList")
		pro = gtk.gdk.pixbuf_new_from_file('images/flickr_pro.gif')
		imagerenderer = gtk.CellRendererPixbuf()
		column_pro = gtk.TreeViewColumn('Pro', imagerenderer, pixbuf=1)


		textrenderer = gtk.CellRendererText()
		column_login = gtk.TreeViewColumn("Login", textrenderer, text=2, font=0)
		column_password = gtk.TreeViewColumn("Password", textrenderer, text=3, font=0)


		self.treeview.append_column(column_pro)
		self.treeview.append_column(column_login)
		self.treeview.append_column(column_password)

		self.accounts_model = gtk.ListStore(str, gtk.gdk.Pixbuf, str, str, str)
		self.treeview.set_model(self.accounts_model)


		self.reload_account_list()
		self.window.show_all()

	def reload_account_list(self):
		self.preferences = SettingsHandler()
		accounts = self.preferences.get_accounts()
		self.accounts_model.clear()
		for account in accounts:
			icon=None
			if account[3] == "True":
				icon=pro
			font="sans 12"
			if account[2] == "True":
				font="sans bold 12"
			self.accounts_model.append([font, icon, account[0], '[secret]', account[1]])

		
	def remove_selected_account(self, treeiter, account):
		self.preferences.remove_account(account)
		self.accounts_model.remove(treeiter)

	def on_AccountAddButton_clicked(self, *args):
		login = self.builder.get_object("LoginAccountEntry").get_text()
		password = self.builder.get_object("PasswordAccountEntry").get_text()
		default = self.builder.get_object("DefaultAccountCB").get_active()

		account_default = "False"
		if default is True:
			account_default = "True"

		if login == "" or password == "":
			dm = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT,
                             gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,
                             "Error to add account. Login or password empty!")
			dm.run()
			dm.destroy()
		else:
			if not self.preferences.add_account(login, password, account_default, "False"):
				dm = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,
                               "Error to add account. Account already exists or "\
                                "already have a default account!")
				dm.run()
				dm.destroy()
		self.reload_account_list()

	def on_IconViewPreferences_selection_changed(self, *args):
		try:
			current = args[0].get_selected_items()[0][0]
			self.notebook.set_current_page(current)
		except:
			pass

	def on_AccountRemoveButton_clicked(self, *args):
		dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
                               gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                               "Are you sure?")

		selection = self.treeview.get_selection()
		model, treeiter = selection.get_selected()
		model, treepath = selection.get_selected_rows()
		if treeiter is not None:
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				self.remove_selected_account(treeiter, model[treepath[0][0]][2])

	def on_OkButton_clicked(self, *args):
		self.on_PreferencesDialog_destroy(None)

	def on_PreferencesDialog_destroy(self, *args):
		self.window.destroy()

