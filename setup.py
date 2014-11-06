import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='MCRcon',
      version='1.0',
      py_modules=['mcrcon'],
      description='MCRcon',
      author='F. Anderson, B. Gale',
      author_email='finnian@fxapi.co.uk, barney.gale@gmail.com',
      url='https://github.com/developius/MCRcon',
      long_description=read('README.md'),
      )