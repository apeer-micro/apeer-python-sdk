# APEER Python SDK

[![Build Status](https://travis-ci.com/apeer-micro/apeer-python-sdk.svg?branch=master)](https://travis-ci.com/apeer-micro/apeer-python-sdk)
[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI Version](https://img.shields.io/pypi/v/apeer-dev-kit.svg)](https://pypi.org/project/apeer-dev-kit/)
[![License](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](https://github.com/apeer-micro/apeer-python-sdk/blob/master/LICENSE.txt)

## What it does

Our APEER Python SDK aka. **a**peer-**d**ev-**k**it (ADK) is a Python library for reading inputs and writing outputs of [APEER](https://www.apeer.com) modules. The ADK will take care of reading inputs from previous modules in APEER and writing your outputs in the correct format for the next module.

## Installation

```shell
$ pip install apeer-dev-kit
```

## How to Use

Your code (your_code.py) can be in it's seperate package and run totally independent of APEER if you use the following structure for `__main__`.

```python
#### apeer_main.py ####

from apeer_dev_kit import adk
import your_code

if __name__ == '__main__':
    inputs = adk.get_inputs()

    outputs = your_code.run(inputs['input_image_path'], inputs['red'], inputs['green'], inputs['blue'])

    adk.set_output('success', outputs['success'])
    adk.set_file_output('tinted_image', outputs['tinted_image'])
    adk.finalize()


#### your_code.py #####

def run(input_image_path, red, green, blue):

    # your processing code goes here ...

    # Make sure you return the outputs as a dictionary containing all output
    # values as specified for your APEER module
    return {'success': True, 'tinted_image': output_file_path}

```
