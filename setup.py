from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='apeer-dev-kit',
      version='1.0.6',
      description='Development kit for creating modules on apeer',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/apeer-micro/apeer-python-sdk',
      author='apeer-micro',
      packages=['apeer_dev_kit'],
      classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],)
