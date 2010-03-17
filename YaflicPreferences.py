#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import gtk, gobject
import os

class YaflicPreferences(object):
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("glade/yaflic-preferences.glade")
		self.dialog = builder.get_object("PreferencesDialog")
		self.categories = builder.get_object("PreferencesCategories")

		builder.connect_signals(self)

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

	def on_OkButton_clicked(self, *args):
		self.on_PreferencesDialog_destroy(None)

	def on_PreferencesDialog_destroy(self, *args):
		self.dialog.destroy()

