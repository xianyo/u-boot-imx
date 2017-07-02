#
# (C) Copyright 2010 Freescale Semiconductor, Inc.
#
#See file CREDITS for list of people who contributed to this
#project.
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License as
#published by the Free Software Foundation; either version 2 of
#the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#MA 02111-1307 USA
#
# --------------------------------------------------------------------------------------
#		bin2txt.pyw
#
#  Description: Convert bin to txt format, ^_^.
#  Python version: Python 2.3.2 or higher
#  Version: 1.00 DEMO
#  Date:    25-10-2010
#  Author:  Terry Lu <Terry.Lui@gmail.com>
#
#  History:
#  25-10-2010 1.00 Initial written.
# --------------------------------------------------------------------------------------

import sys
import os
#import time
import string
#import math	# For sqrt() function.
import struct

#from Tkinter import *
import Tkinter
#import tkMessageBox

def Print_Help():
	'''  Print how to use this script, ^_^ '''
	print '\n'
	print '+--------------------------------------------------------------+'
	print 'Usage:\n'
	print '		python bin2txt.pyw <filename>'
	print ' <filename> - Contain the data.'
	print ' The output file will be filename.data.'
	print '+--------------------------------------------------------------+'

def Print_Version():
	''' Print the version info, ^_^ '''
	print '+--------------------------------------------------------------+'
	print '			bin2txt.pyw\n'
	print '+Description: Convert hex to txt format, ^_^.'
	print '+Python version: Python 2.3.2 or higher'
	print '+Version: 1.00 DEMO'
	print '+Date:    25-10-2010'
	print '+Author:  Terry Lu'
	print '+--------------------------------------------------------------+'

def ShowErrorMessageBox(error_string):
	Tkinter.Tk().withdraw()
	tkMessageBox.showerror('Error',error_string)
	
def ShowSuccessMessageBox(success_string):
	Tkinter.Tk().withdraw()
	tkMessageBox.showinfo('Success',success_string)		

def BinStr2Int(strBin):
	''' Convert a binary number string to integer. '''
	intDataVal = 0
	for each_char in strBin:
		intDataVal = intDataVal * 2 + int(each_char)
	return intDataVal

def Main_Run(argv_list):
	'''
	Main app to run like main() in C, ^_^
	Option included:
		-version : Prints the version info
		-help    : Display help info
    '''

	# The number of args
	argc = len(argv_list)

	# Error string
	error_string = ''

	# Define the hs files path
	hex_file_path = ''
	hex_filename  = ''

	if 2 == argc:
		if argv_list[1].startswith('-'):
			# fetch the option
			option = argv_list[0][1:]
			if 'version' == option:
				Print_Version()
			elif 'help' == option:
				Print_Help()
			else:
				print 'Unknown', option, 'option!'
		else:
			# sys.argv[1] is a path without filename
			hex_filename = argv_list[1]
			if os.path.isdir(hex_filename):
				Print_Help()
				return
			elif not os.path.exists(hex_filename):
				print 'File not found!'
				return
	else:
		Print_Help()
		return

	# Target output file path
	target_txt_filename = ''.join((os.getcwd(), os.sep, hex_filename, '.h'))
	target_file_obj = open(target_txt_filename, 'w')

	try:
		hex_file_obj = open(hex_filename, "rb").read()
	except IOError:
		print 'Read file IO error!'
		return		

	file_size = os.path.getsize(hex_filename)
	print "file_size:%d" % (file_size)
	file_start, file_stop = 0, struct.calcsize('B' * file_size)
	print "file_start:%d, file_stop:%d" % (file_start, file_stop)
	print "str_len:%d" % (len(hex_file_obj[file_start : file_stop]))
	data_words = struct.unpack('B' * file_size, hex_file_obj[file_start : file_stop])

	str_text_name = hex_filename.replace(".bmp","_") + 'logo_bmp'
	str_text_name_size = str_text_name+'_size'
	str_word_data = ''
	str_text_data = ''
	str_text_data += 'unsigned char '+ str_text_name + '[] = {\n\t'
	counter = 0
	for each_words in data_words:
		if (counter > 6):
			str_word_data = ", 0x%02lx,\n\t" % (each_words)
			counter = 0
		else:
			if 0 == counter:
				str_word_data = "0x%02lx" % (each_words)
			else:
				str_word_data = ", 0x%02lx" % (each_words)
			counter += 1
		str_text_data += str_word_data
		
	str_text_data += "\n};"

	str_text_data += '\nint ' + str_text_name_size + ' = sizeof(' + str_text_name +');'
	target_file_obj.write(str_text_data)
	target_file_obj.close()

# Run script
Main_Run(sys.argv)

# For test
#if __name__ == '__main__':
#	pass
