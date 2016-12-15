from distutils.core import setup
setup(
  name = 'remrunner',
  packages = ['remrunner'], 
  version = '0.4',
  description = 'Transfer a local script file to a remote host and execute it.',
  long_description=read('README.rst'),
  author = 'Jeff Leary',
  author_email = 'sillymonkeysoftware@gmail.com',
  url = 'https://github.com/jeffleary00/remrunner',
  download_url = 'https://github.com/jeffleary00/remrunner/tarball/0.4',
  # install_requires = ['paramiko'],
  keywords = ['automation', 'ssh', 'command', 'paramiko'],
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
  ],
)
