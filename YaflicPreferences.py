#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import gtk, gobject
import os
from SettingsHandler import *

class YaflicPreferences(object):
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("glade/yaflic-preferences.glade")
		self.dialog = builder.get_object("PreferencesDialog")
		self.categories = builder.get_object("PreferencesCategories")
		self.treelist = builder.get_object("treeview1")
		self.notebook = builder.get_object("notebook1")

		builder.connect_signals(self)

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

		pro = gtk.gdk.pixbuf_new_from_file('images/flickr_pro.gif')
		imagerenderer = gtk.CellRendererPixbuf()
		column_pro = gtk.TreeViewColumn('Pro', imagerenderer, pixbuf=0)

		textrenderer = gtk.CellRendererText()
		column_login = gtk.TreeViewColumn("Login", textrenderer, text=1)
		column_password = gtk.TreeViewColumn("Password", textrenderer, text=2)

		self.treelist.append_column(column_pro)
		self.treelist.append_column(column_login)
		self.treelist.append_column(column_password)

		model2 = gtk.ListStore(gtk.gdk.Pixbuf, str, str)
		self.treelist.set_model(model2)

		preferences = SettingsHandler()
		accounts = preferences.get_accounts()
		for account in accounts:
			model2.append([pro, account[0], account[1]])

		self.dialog.show_all()

	def on_AccountAddButton_clicked(self, *args):
		dm = gtk.MessageDialog(self.dialog, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE, "Error to add account. Empty login!")
		dm.run()
		dm.destroy()

			
	def on_PreferencesCategories_selection_changed(self, *args):
		try:
			current = args[0].get_selected_items()[0][0]
			self.notebook.set_current_page(current)
		except:
			pass

	def on_OkButton_clicked(self, *args):
		self.on_PreferencesDialog_destroy(None)

	def on_PreferencesDialog_destroy(self, *args):
		self.dialog.destroy()

