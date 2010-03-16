#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import gtk, gobject
import os

class YaflicPreferences(object):
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("yaflic-preferences.glade")
		builder.connect_signals({ "on_PreferencesDialog_destroy" : gtk.main_quit })
		self.dialog = builder.get_object("PreferencesDialog")
		self.categories = builder.get_object("PreferencesCategories")

		model = gtk.ListStore(str, gtk.gdk.Pixbuf)
		pixbuf = gtk.gdk.pixbuf_new_from_file('images/prefs_general.png')
		model.append(['General', pixbuf])

		pixbuf = gtk.gdk.pixbuf_new_from_file('images/prefs_security.png')
		model.append(['Security', pixbuf])

		self.categories.set_item_width(94)

		self.categories.set_text_column(0)
		self.categories.set_pixbuf_column(1)

		self.categories.set_model(model)

		while gtk.events_pending():
			gtk.main_iteration()


		self.dialog.show()

if __name__ == "__main__":
	dialog  = YaflicPreferences()
	gtk.main()
