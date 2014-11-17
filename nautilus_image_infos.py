#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nautilus_image_infos : Nautilus extension that display several image informations in Nautilus explorer columns

# By @Brunus_V
# version : alpha 2
# Last update : 2014 Nov. 17
# Licence :  WTFPL
# http://www.wtfpl.net/

# Requierements :
# Tu run this extension you need : python-imaging python-nautilus python-pyexiv2

# Installation :
# Copy this script in your ~/.local/share/nautilus-python/extensions/
# Kill Nautilus if already running : mautilus -q
# Open Nautilus explorer window and go in Edit/preferences/Columns list to check the new columns you want to display
# Browse a directory cointaining images, choose list as display mode to show columns

import os
import urllib
from gi.repository import Nautilus, GObject
import pyexiv2
import Image

class ColumnExtension(Nautilus.ColumnProvider, Nautilus.InfoProvider, GObject.GObject):

	def get_columns(self):
		return (
			# exif support
			Nautilus.Column(
				name='NautilusPython::exif_pixeldimensions_column',
				attribute='exif_pixeldimensions',
				label='EXIF Image Size',
				description='EXIF Image size - pixel dimensions'),
			Nautilus.Column(
				name='NautilusPython::pixeldimensions_column',
				attribute='pixeldimensions',
				label='Image Size',
				description='Image size - pixel dimensions'),
		)

	def update_file_info(self, fileobj):
		if fileobj.get_uri_scheme() != 'file':
			return

		filename = urllib.unquote(fileobj.get_uri()[7:])
		
		# jpeg EXIF handling (also try running it on other image types, if only for the image size)
		if fileobj.is_mime_type('image/jpeg') or fileobj.is_mime_type('image/png') or fileobj.is_mime_type('image/gif') or fileobj.is_mime_type('image/bmp'):
			try:
				img = pyexiv2.Image(filename)
				img.readMetadata()
				fileobj.add_string_attribute('exif_pixeldimensions',str(img['Exif.Photo.PixelXDimension'])+'x'+str(img['Exif.Photo.PixelYDimension']))
			except:
				# no exif data?

				fileobj.add_string_attribute('exif_pixeldimensions',"")
			# try read image info directly
			try:
				im = Image.open(filename)
				fileobj.add_string_attribute('pixeldimensions',str(im.size[0])+'x'+str(im.size[1]))
			except:
				fileobj.add_string_attribute('pixeldimensions',"[image read error]")
		else:
			fileobj.add_string_attribute('exif_pixeldimensions', '')
			fileobj.add_string_attribute('pixeldimensions', '')

		self.get_columns()
