#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import gtk, gobject
import os
from YaflicPreferences import *

class Yaflic(object):
	def __init__(self):
		self.thumb_width = 128
		self.thumb_height = 128
		self.thumb_inside_hmarging = 50

		builder = gtk.Builder()
		builder.add_from_file("glade/yaflic.glade")
		self.window = builder.get_object("MainWindow")
		builder.connect_signals(self)
		self.imageview = builder.get_object("ImageView")
		self.progressbar = builder.get_object("ProgressBar")
		self.loadbutton = builder.get_object("RefreshImages")
		self.imagezoom = builder.get_object("ImageZoom")
		self.zoomless = builder.get_object("ZoomLess")
		self.zoommore = builder.get_object("ZoomMore")
		self.window.maximize()
		self.imagezoom.set_range(0,100)
		self.imagezoom.set_increments(10,100)

	def on_RefreshImages_clicked(self, *args):
		self.generate_default_thumbs("temp/")

	def on_MainWindow_destroy(self, *args):
		gtk.main_quit()

	def on_PreferencesMenu_activate(self, *args):
		preferences = YaflicPreferences()
		#gtk.main_quit()

	def change_cursor(self, object, cursor):
		if cursor is None:
			object.window.set_cursor(None)
		else:
			new_cursor = gtk.gdk.Cursor(cursor)
			object.window.set_cursor(new_cursor)

	def generate_default_thumbs(self, dir):
		# TODO: Make this as a thread;
		# TODO: Make cache thumbs to improve peformance;
		files = os.listdir(dir)
		
		self.store = gtk.ListStore(str, gtk.gdk.Pixbuf)
		self.imageview.set_item_width(self.thumb_width + self.thumb_inside_hmarging)
		
		self.start_progress(len(files))

		self.imageview.set_text_column(0)
		self.imageview.set_pixbuf_column(1)
	
		for file in files:
			filename = dir + file
			pixbuf =  gtk.gdk.pixbuf_new_from_file_at_scale(filename, self.thumb_width, self.thumb_height, True)
			self.store.append([file, pixbuf])
	
			self.imageview.set_model(self.store)
	
			while gtk.events_pending():
				gtk.main_iteration()

			self.progress_timeout(self.progressbar, len(files))

		self.stop_progress()
		

	def start_progress(self, len):
		self.progressbar.set_fraction(0)
		self.change_cursor(self.window, gtk.gdk.WATCH)
		self.progressbar.show()

	def stop_progress(self):
		self.change_cursor(self.window, None)
		self.progressbar.hide()

	def progress_timeout(self, pbobj, images_len):
		current_value = pbobj.get_fraction()
		if current_value >= 1.0:
			new_val = (1 / float(images_len))
		else:
			new_val = current_value + (1 / float(images_len))
		pbobj.set_fraction(new_val)

		return True


if __name__ == "__main__":
	app = Yaflic()
	app.window.show_all()
	app.progressbar.hide()
	gtk.main()
