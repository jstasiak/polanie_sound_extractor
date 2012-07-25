#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Polanie sound.dat samples extractor.

Jakub Stasiak
jakub@stasiak.at
'''

from os.path import exists, isdir, join
from os import makedirs, remove
from struct import unpack
from subprocess import check_call

import sys

def extract(file_name, directory, count):
	'''
	Extracts samples from archive to specified directory and performs conversion
	to WAV afterwards.
	'''

	with open(file_name, mode = 'rb') as input_file:
		buf = input_file.read()

	lengths = samples_lengths(buf, count)
	boundaries = samples_boundaries(lengths)

	if not exists(directory):
		makedirs(directory)

	for i, (start, stop) in enumerate(boundaries):
		raw_file = join(directory, '{0}.raw'.format(unicode(i).zfill(3)))
		with open(raw_file, 'wb') as output:
			output.write(buf[start:stop])

		wav_file = raw_file.replace('.raw', '.wav')

		# Sox parameters found experimentally
		check_call(['sox', '-r', '22050', '-u', '-c', '1', '-b', '8',
			raw_file, wav_file])

		remove(raw_file)

	print('Success!')


def samples_lengths(data, count):
	'''
	Gets samples lengths from raw data. Samples count has to be know prior to
	extracting the information.
	'''

	# Samples lengths are serialized 4-byte little-endian integers.
	single_size = 4
	lengths_all_bytes = data[-single_size * count:]
	lengths_bytes = [lengths_all_bytes[single_size * index : single_size * (index + 1)] for index in range(count)]
	lengths = [unpack('<i', element)[0] for element in lengths_bytes]
	return lengths

def samples_boundaries(lengths):
	'''
	Returns tuples (start, stop) based on samples lengths.
	'''
	current_offset = 0

	boundaries = []
	for l in lengths:
		boundaries.append((current_offset, current_offset + l))
		current_offset += l
		
	return boundaries
	

def main():
	if len(sys.argv) != 3:
		print('Usage: {0} SOUND_DAT_FILE OUTPUT_DIRECTORY'.format(sys.argv[0]))
		exit(1)

	file_name, directory = sys.argv[1:]
	extract(file_name, directory, count = 183)

if __name__ == '__main__':
	main()
