from apeer_dev_kit import _core

_adk = _core._core()


def get_inputs():
    """ Get inputs inside your module """
    return _adk._get_inputs()


def set_output(key, value):
    """ Set the output """
    _adk._set_output(key, value)


def set_file_output(key, filepath):
    """ Set the output """
    _adk._set_file_output(key, filepath)


def finalize():
    """ This method should be called at the end """
    _adk._finalize()
