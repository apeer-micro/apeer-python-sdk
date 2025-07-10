import io, os
from setuptools import setup

# read __version__ without importing the package
def read_version():
    here = os.path.abspath(os.path.dirname(__file__))
    init_py = os.path.join(here, "apeer_dev_kit", "__init__.py")
    for line in io.open(init_py, encoding="utf-8"):
        if line.startswith("__version__"):
            # __version__ = "1.3.0"
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("Unable to find __version__ in apeer_dev_kit/__init__.py")

__version__ = read_version()

setup(name='apeer-dev-kit',
      version=__version__,
      description='Development kit for creating modules on apeer',
      url='https://github.com/apeer-micro/apeer-python-sdk',
      author='apeer-micro',
      packages=['apeer_dev_kit'],
      python_requires='>=3.8, <3.14',
      install_requires=[],
      classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description="""
APEER Python SDK aka (ADK) is a Python library for reading inputs and writing outputs of APEER(https://www.apeer.com) modules.
The ADK will take care of reading inputs from previous modules in APEER and writing your outputs in the correct format for the next mod ule.
This project is hosted at https://github.com/apeer-micro/apeer-python-sdk
The documentation can be found at https://github.com/apeer-micro/apeer-python-sdk/blob/master/README.md
""")