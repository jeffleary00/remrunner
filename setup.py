import os
from distutils.core import setup

contents = ""
if os.path.exists('README.rst'):
    readme = open('README.rst', 'r')
    contents = readme.read()
    
setup(
  name = 'remrunner',
  packages = ['remrunner'], 
  version = '0.5',
  description = 'Transfer a local script file to a remote host and execute it.',
  long_description=contents,
  author = 'Jeff Leary',
  author_email = 'sillymonkeysoftware@gmail.com',
  url = 'https://github.com/jeffleary00/remrunner',
  download_url = 'https://github.com/jeffleary00/remrunner/tarball/0.5',
  # install_requires = ['paramiko'],
  keywords = ['automation', 'ssh', 'command', 'paramiko'],
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
  ],
)
