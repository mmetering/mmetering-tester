from distutils.core import setup
import py2exe

setup(name='MMetering Tester',
      version='0.1',
      description='GUI testing tool for windows in order to check reachability of connected meters',
      long_description='\n\n'.join([open('README.md').read()]),
      author='Christoph Sonntag',
      author_email='info@mmetering.chrisonntag.com',
      url='https://mmetering.chrisonntag.com/',
      install_requires=['minimalmodbus', 'pyserial'],
      console=['application.main.py'],
      )
