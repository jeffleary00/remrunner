from distutils.core import setup
setup(
  name = 'remrunner',
  packages = ['remrunner'], # this must be the same as the name above
  version = '0.1',
  description = 'Transfer a local script file to a remote host and execute it.',
  author = 'Jeff Leary',
  author_email = 'sillymonkeysoftware@gmail.com',
  url = 'https://github.com/jeffleary00/remrunner', # use the URL to the github repo
  download_url = 'https://github.com/jeffleary00/remrunner/tarball/0.1', # I'll explain this in a second
  keywords = ['automation', 'ssh', 'command', 'paramiko'], # arbitrary keywords
  classifiers = [],
)