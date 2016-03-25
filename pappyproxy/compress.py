#!/usr/bin/env python

import crochet
import glob
import pappyproxy

import zipfile
import tarfile

# This is a gross hack, please help
bz2 = None
try:
    import bz2
except:
    print "BZ2 not installed on your system"

from base64 import b64encode, b64decode
from os import getcwd, sep, path, urandom 

class Compress(object):
    def __init__(self, sessconfig):
        self.config = sessconfig
        self.zip_archive = sessconfig.archive
        self.bz2_archive = sessconfig.archive

    def compress_project():
        if bz2:
            tar_project()
        else:
            zip_project()
    
    def decompress_project():
        if bz2:
            untar_project()
        else:
            unzip_project()
    
    def zip_project():
        """
        Zip project files
    
        Using append mode (mode='a') will create a zip archive
        if none exists in the project.
        """
        try:
            zf = zipfile.ZipFile(self.zip_archive, mode="a")
            project_files = self.config.get_project_files() 
            for pf in project_files:
                zf.write(pf)
            zf.close()
        except e:
            raise PappyException("Error creating the zipfile", e)
        pass
    
    def unzip_project():
        """
        Extract project files from decrypted zip archive.
        Initially checks the zip archive's magic number and
        attempts to extract pappy.json to validate integrity 
        of the zipfile.
        """
        if not zipfile.is_zipfile(self.zip_archive):
            raise PappyException("Project archive corrupted.")
    
        zf = zipfile.ZipFile(self.zip_archive)
    
        try:
            zf.extract("config.json")
        except e:
            raise PappyException("Project archive contents corrupted. Error: ", e)
    
        zf.extractall()
    
    def tar_project():
        if tarfile.is_tarfile(self.bz2_archive):
            archive = tarfile.open(self.bz2_archive, 'w:bz2')
            project_files = self.config.get_project_files()
    
            # Read files line by line to accomodate larger files, e.g. the project database
            for pf in project_files:
                archive.add(pf)
    	archive.close()
    
    def untar_project():
        if tarfile.is_tarfile(self.bz2_archive):
            # Attempt to read the first 16 bytes of the archive
            # Raise exception if there is a failure
    	    project_files = self.config.get_project_files()
            try:
                with tarfile.open(self.bz2_archive, "r:bz2") as archive:
                    for pf in project_files:
                        archive.add(pf)
            except e:
                raise PappyException("Project archive contents corrupted. Error: ", e)
