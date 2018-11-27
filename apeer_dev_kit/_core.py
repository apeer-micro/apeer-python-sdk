import os
import json

from ._utility import copyfile

class _core:
    def __init__(self):
        try:
            self._outputs = {}
            self._wfe_output_params_file = ''
            self._input_json = json.loads(os.environ['WFE_INPUT_JSON'])
        except KeyError:
            raise KeyError(
                'Environment variable WFE_INPUT_JSON not found. Please add WFE_INPUT_JSON as an environment variale to get inputs')

    def _get_inputs(self):
        """ Get the inputs"""
        try:
            self._wfe_output_params_file = self._input_json.pop(
                'WFE_output_params_file')
            return self._input_json
        except KeyError:
            raise KeyError(
                'Key WFE_output_params_file not found. Please add WFE_output_params_file in input json')

    def _set_output(self, key, value):
        if (key is None) or (value is None):
            raise TypeError("key or value cannot be None")
        self._outputs[key] = value

    def _set_file_output(self, key, filepath):
        if isinstance(filepath, list):
            dsts = []
            for f in filepath:
                if(not f or f.isspace()):
                    print("Empty filepath, skipping")
                    continue
                if(f.startswith("/output/")):
                    dsts.append(f)
                else:
                    dst = "/output/" + os.path.basename(f)
                    copyfile(f, dst)
                    dsts.append(dst)
            if(len(dsts) > 0):
                self._outputs[key] = dsts
        else:
            if(not filepath or filepath.isspace()):
                print("Empty filepath, skipping")
                return
            if(filepath.startswith("/output/")):
                dst = filepath
            else:
                dst = "/output/" + os.path.basename(filepath)
                copyfile(filepath, dst)
            self._outputs[key] = dst

    def _finalize(self):
        with open("/output/" + self._wfe_output_params_file, 'w') as fp:
            json.dump(self._outputs, fp)
