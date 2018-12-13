import os
import json
import logging as log

from ._utility import copyfile

class _core:
    def __init__(self):
        log.basicConfig(format='%(asctime)s [ADK:%(levelname)s] %(message)s', level=log.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        try:
            log.info('Initializing')
            self._outputs = {}
            self._wfe_output_params_file = ''
            self._input_json = json.loads(os.environ['WFE_INPUT_JSON'])
            log.info('Found module\'s inputs to be {}'.format(self._input_json))
        except KeyError:
            message = 'Environment variable WFE_INPUT_JSON not found'
            log.error(message)
            raise KeyError(message)

    def _get_inputs(self):
        ''' Get the inputs'''
        try:
            self._wfe_output_params_file = '/output/' + self._input_json.pop('WFE_output_params_file')
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
                if(f.startswith('/output/')):
                    dsts.append(f)
                else:
                    dst = '/output/' + os.path.basename(f)
                    log.info('Copying file "{}" to "{}"'.format(os.path.basename(f), dst))
                    copyfile(f, dst)
                    dsts.append(dst)
            if(len(dsts) > 0):
                self._set_output(key, dsts)
        else:
            if(not filepath or filepath.isspace()):
                log.warn('Empty filepath, skipping')
                return
            if(filepath.startswith('/output/')):
                dst = filepath
            else:
                dst = '/output/' + os.path.basename(filepath)
                log.info('Copying file "{}" to "{}"'.format(os.path.basename(filepath), dst))
                copyfile(filepath, dst)
            self._set_output(key, dst)

    def _finalize(self):
        with open(self._wfe_output_params_file, 'w') as fp:
            json.dump(self._outputs, fp)
        log.info('Module finalized')
