from setuptools import setup
from apeer_dev_kit import __version__

setup(name='apeer-dev-kit',
      version=__version__,
      description='Development kit for creating modules on apeer',
      url='https://github.com/apeer-micro/apeer-python-sdk',
      author='apeer-micro',
      packages=['apeer_dev_kit'],
      classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description="""
APEER Python SDK aka (ADK) is a Python library for reading inputs and writing outputs of APEER(https://www.apeer.com) modules.
The ADK will take care of reading inputs from previous modules in APEER and writing your outputs in the correct format for the next mod ule.
This project is hosted at https://github.com/apeer-micro/apeer-python-sdk
The documentation can be found at https://github.com/apeer-micro/apeer-python-sdk/blob/master/README.md
""")