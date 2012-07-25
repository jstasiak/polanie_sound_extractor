What's that
===========

This application allows you to extract sound samples from Polanie (1996 Polish RTS game) original sound archive file.


Requirements
============

* Python 2.x >= 2.6
* sox

Usage
=====

python extractor.py SOUND_DAT OUTPUT_DIRECTORY


File format
===========

File (at least the version I have) consists of 183 sound samples. Samples are tightly packed one after another. At the end of sound.dat file there is 183 serialized 4-byte little-endian integers which contain sample sizes.

Samples consist of raw 1-channel, 8-bit width, 22050 Hz unsigned integer sound data. Application calls sox to convert this data to WAV files.

Author
======

Jakub Stasiak <jakub@stasiak.at>
