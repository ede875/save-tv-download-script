#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# To build a distribution zip file for this package, run from within this directory:
#   python setup.py build sdist

'''
Save.TV Download Script

Prerequisites:
- Python 2.6 or 2.7
- Python package "mechanize" (see http://pypi.python.org/pypi/mechanize/,
  or install via pip: 'pip install mechanize')
- wget (see http://www.gnu.org/software/wget/)
- A Save.TV account (see http://www.save.tv/)
- An Internet connection
'''

from distutils.core import setup
import sys, os


def include_file( path, moniker, install=True):
    '''Determine whether a customizable file is to be installed, based upon
prior existence of the file, and print messages when invoked for install.

    path        Path name of the customizable file.
    moniker     Text for recognizing the file.
    install     Boolean controlling whether the file is to be installed.
'''

    if 'install' in sys.argv:
        if install:
            try:
                os.stat(path)
            except Exception:
                include_it = True
                print "=" * 79
                print "---> Please edit and customize the newly installed "+moniker+": "+path
                print "=" * 79
            else:
                include_it = False
                print "Info: Will not replace the existing "+moniker+": "+path
        else:
            include_it = False
            print "Info: Will not install the "+moniker+": "+path
    else:
        # some package build -> we include the file silently.
        include_it = True

    return include_it


include_configfile = include_file(sys.prefix + os.sep + "scripts" + os.sep + "savetv.cfg", "config file")
include_unixscript = include_file(sys.prefix + os.sep + "scripts" + os.sep + "run_save.tv_download", "Unix/Linux start script", os.sep == "/")
include_winscript  = include_file(sys.prefix + os.sep + "scripts" + os.sep + "run_save.tv_download.bat", "Windows start script", os.sep == "\\")

data_files = []
if include_configfile:
    data_files.append(('scripts', ['savetv.cfg']))

script_files = ['stvDld.py']
if include_unixscript:
    script_files.append('run_save.tv_download')
if include_winscript:
    script_files.append('run_save.tv_download.bat')

setup(
    name             = 'stvdld',
    version          = '0.3_jocon.1',
    description      = 'Save.TV Download Script',
    long_description = __doc__,
    author           = 'proselyt',
    author_email     = 'proselyt@googlemail.com',
    url              = 'http://code.google.com/p/save-tv-download-script/',
    platforms        = ['any'],
    py_modules       = ['SaveTvDownloadWorker', 'SaveTvEntity'],
    data_files       = data_files,
    scripts          = script_files,
    classifiers      = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users",
        "Environment :: Console",
        "Topic :: Video",
    ],
    license          = 'GPL v3 (see http://www.gpl.org/)',
    # options supported only if we used setuptools:
    #keywords         = "Save.TV Movies Video",
    #install_requires = [
    #],
)
