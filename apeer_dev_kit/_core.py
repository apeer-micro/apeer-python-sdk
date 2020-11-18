import os
import json
import logging as log
import pkg_resources

from apeer_dev_kit import __version__
from ._utility import copyfile

class _core:
    WFE_INPUT_ENV_VARIABLE = 'WFE_INPUT_JSON'

    def __init__(self):
        log.basicConfig(format='%(asctime)s [ADK:%(levelname)s] %(message)s', level=log.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        log.info('Initializing ADK v' + __version__)
        self._outputs = {}
        self._wfe_output_params_file = ''
        if os.name == 'nt':
            self.output_dir = 'C:\\output\\'
            self.wfe_input_file_name = 'C:\\params\\WFE_input_params.json'
        else:
            self.output_dir = '/output/'
            self.wfe_input_file_name = '/params/WFE_input_params.json'
        self._input_json = self._read_inputs()
        log.info('Found module\'s inputs to be {}'.format(self._input_json))

    def _read_inputs(self):
        ''' Read inputs either from file or from environment variable'''
        try:
            if self.WFE_INPUT_ENV_VARIABLE in os.environ:
                return json.loads(os.environ[self.WFE_INPUT_ENV_VARIABLE])
            else:
                with open(self.wfe_input_file_name, 'r') as input_file:
                    return json.load(input_file)
        except IOError:
            message = 'Input file {} not found'.format(self.wfe_input_file_name)
            log.error(message)
            raise IOError(message)
        except AttributeError:
            message = 'ADK not initialized'
            log.error(message)
            raise IOError(message)

    def _get_inputs(self):
        ''' Get the inputs'''
        try:
            self._wfe_output_params_file = self.output_dir + self._input_json.pop('WFE_output_params_file')
            log.info('Outputs will be written to {}'.format(self._wfe_output_params_file))
            return self._input_json
        except KeyError:
            message = 'Key WFE_output_params_file not found'
            log.error(message)
            raise KeyError(message)

    def _set_output(self, key, value):
        log.info('Set output "{}" to "{}"'.format(key, value))
        if (key is None) or (value is None):
            message = 'key or value cannot be None'
            log.error(message)
            raise TypeError(message)
        self._outputs[key] = value

    def _set_file_output(self, key, filepath):
        if isinstance(filepath, list):
            dsts = []
            for f in filepath:
                if(not f or f.isspace()):
                    log.warn('Empty filepath, skipping')
                    continue
                if(f.startswith(self.output_dir)):
                    dsts.append(f)
                else:
                    dst = self.output_dir + os.path.basename(f)
                    log.info('Copying file "{}" to "{}"'.format(os.path.basename(f), dst))
                    copyfile(f, dst)
                    dsts.append(dst)
            if(len(dsts) > 0):
                self._set_output(key, dsts)
        else:
            if(not filepath or filepath.isspace()):
                log.warn('Empty filepath, skipping')
                return
            if(filepath.startswith(self.output_dir)):
                dst = filepath
            else:
                dst = self.output_dir + os.path.basename(filepath)
                log.info('Copying file "{}" to "{}"'.format(os.path.basename(filepath), dst))
                copyfile(filepath, dst)
            self._set_output(key, dst)

    def _finalize(self):
        with open(self._wfe_output_params_file, 'w') as fp:
            json.dump(self._outputs, fp)
        log.info('Module finalized')
