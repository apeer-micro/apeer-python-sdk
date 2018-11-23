# APEER Python SDK

## What it does

Our **A**PEER Python S**DK** (ADK) is a Python library for reading inputs and writing outputs of [APEER](https://www.apeer.com) modules. The ADK will take care of reading inputs from previous modules in APEER and writing your outputs in the correct format for the next module.

## Installation

```shell
$ pip install <coming soon>
```

## How to Use

Your code (your_code.py) can be in it's seperate package and run totally independent of APEER if you use the following structure for `__main__`.

```python
#### apeer_main.py ####

from apeer_dev_kit import adk
import your_code

if __name__ == "__main__":
    inputs = adk.get_inputs()

    outputs = your_code.run(inputs.input_image_path, inputs.red, inputs.green, inputs.blue)

    adk.set_output("success", outputs.success)
    adk.set_file_output("tinted_image", outputs.tinted_image)
    adk.finalize()


#### your_code.py #####

def run(input_image_path, red, green, blue):

    # your processing code goes here ...

    # Make sure you return the outputs as a dictionary containing all output
    # values as specified for your APEER module
    return { "success": True, "tinted_image": output_file_path }

```
