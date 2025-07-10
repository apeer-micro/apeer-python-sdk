import unittest
import sys
import os
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apeer_dev_kit import _core

class TestsCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestsCore, self).__init__(*args, **kwargs)
        if os.name == 'nt':
            self.output_dir = 'C:\\output\\'
        else:
            self.output_dir = '/output/'

    # __init__
    def test_init_givenNoEnvironmentVariableAndNoInputFile_coreIsNotInitialized(self):
        with self.assertRaises(IOError):
            _core._core()

    def test_init_givenEmptyInputJson_coreIsInitialized(self):
        os.environ['WFE_INPUT_JSON'] = '{}'

        core = _core._core()

        self.assertTrue(core)
        self.assertEqual(core._wfe_output_params_file, '')
        self.assertEqual(core._outputs, {})

    def test_init_givenInputJson_coreIsInitalized(self):
        os.environ['WFE_INPUT_JSON'] = '{"WFE_output_params_file":"param.json","red":0.2,"input_image":"test.jpg"}'

        core = _core._core()

        self.assertTrue(core)
        self.assertEqual(core._input_json['WFE_output_params_file'], 'param.json')
    
    # _get_inputs
    def test_get_inputs_givenNoParamFileKey_throwsKeyErrorException(self):
        os.environ['WFE_INPUT_JSON'] = '{"red":0.2,"input_image":"test.jpg"}'
        core = _core._core()

        with self.assertRaises(KeyError):
            core._get_inputs()

    def test_get_inputs_givenInputJson_paramFileIsNotPartOfInputs(self):
        os.environ['WFE_INPUT_JSON'] = '{"WFE_output_params_file":"param.json","red":0.2}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertFalse('WFE_output_params_file' in inputs)
        self.assertEqual(len(inputs), 1)

    def test_get_inputs_givenDecimal_isDeserialized(self):
        os.environ['WFE_INPUT_JSON'] = '{"WFE_output_params_file":"param.json","red":0.2}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs['red'], 0.2)

    def test_get_inputs_givenInteger_isDeserialized(self):
        os.environ['WFE_INPUT_JSON'] = '{"WFE_output_params_file":"param.json","red":2}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs['red'], 2)

    def test_get_inputs_givenString_isDeserialized(self):
        os.environ['WFE_INPUT_JSON'] = '{"WFE_output_params_file":"param.json","value":"testValue"}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs['value'], 'testValue')

    def test_get_inputs_givenBoolean_isDeserialized(self):
        os.environ["WFE_INPUT_JSON"] = '{"WFE_output_params_file":"param.json","value":true}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs["value"], True)

    def test_get_inputs_givenList_isDeserialized(self):
        os.environ["WFE_INPUT_JSON"] = '{"WFE_output_params_file":"param.json","value":["one", "two"]}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs["value"], ["one", "two"])

    # _set_output
    def test_set_output_givenNoneKey_raisesTypeError(self):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        with self.assertRaises(TypeError):
            core._set_output(None, None)

    def test_set_output_givenStringValue_correctlyAdded(self):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_output("test", "string")

        self.assertEqual(core._outputs["test"], "string")

    def test_set_output_givenDecimalValue_correctlyAdded(self):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_output("test", 0.2)

        self.assertEqual(core._outputs["test"], 0.2)

    def test_set_output_givenIntegerValue_correctlyAdded(self):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_output("test", 2)

        self.assertEqual(core._outputs["test"], 2)

    def test_set_output_givenBooleanValue_correctlyAdded(self):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_output("test", True)

        self.assertEqual(core._outputs["test"], True)

    def test_set_output_givenListValue_correctlyAdded(self):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_output("test", ["test1", "test2"])

        self.assertEqual(core._outputs["test"], ["test1", "test2"])

    # _set_file_output
    @mock.patch('apeer_dev_kit._utility.shutil')
    def test_set_file_output_givenEmptyFileName_FileNotCopied(self, mock_shutil):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_file_output("file", "")

        mock_shutil.copyfile.assert_not_called()
        self.assertEqual(mock_shutil.copyfile.call_count, 0)
        self.assertEqual(len(core._outputs), 0)

    @mock.patch('apeer_dev_kit._utility.shutil')
    def test_set_file_output_givenEmptyFileNameList_FileNotCopied(self, mock_shutil):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_file_output("file", ["", " ", '   '])

        mock_shutil.copyfile.assert_not_called()
        self.assertEqual(len(core._outputs), 0)

    @mock.patch('apeer_dev_kit._utility.shutil')
    def test_set_file_output_givenFileNotInOutputFolder_FileCopied(self, mock_shutil):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_file_output("file", "file.txt")

        mock_shutil.copyfile.assert_called_with("file.txt", os.path.join(self.output_dir, "file.txt"))
        self.assertEqual(core._outputs["file"], os.path.join(self.output_dir, "file.txt"))

    @mock.patch('apeer_dev_kit._utility.shutil')
    def test_set_file_output_givenFileInOutputFolder_FileNotCopied(self, mock_shutil):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_file_output("file", os.path.join(self.output_dir, "file.txt"))

        mock_shutil.copyfile.assert_not_called()
        self.assertEqual(core._outputs["file"], os.path.join(self.output_dir, "file.txt"))

    @mock.patch('apeer_dev_kit._utility.shutil')
    def test_set_file_output_givenFileListInOutputFolder_FileNotCopied(self, mock_shutil):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_file_output("file", [os.path.join(self.output_dir, "file1.txt"), os.path.join(self.output_dir, "file2.txt")])

        mock_shutil.copyfile.assert_not_called()
        self.assertEqual(core._outputs["file"], [os.path.join(self.output_dir, "file1.txt"), os.path.join(self.output_dir, "file2.txt")])

    @mock.patch('apeer_dev_kit._utility.shutil')
    def test_set_file_output_givenFileListNotInOutputFolder_FileCopied(self, mock_shutil):
        os.environ["WFE_INPUT_JSON"] = '{}'
        core = _core._core()

        core._set_file_output("file", ["file1.txt", "file2.txt"])

        mock_shutil.copyfile.assert_has_calls([
            mock.call("file1.txt", os.path.join(self.output_dir, "file1.txt")),
            mock.call("file2.txt", os.path.join(self.output_dir, "file2.txt"))])
        self.assertEqual(core._outputs["file"], [os.path.join(self.output_dir, "file1.txt"), os.path.join(self.output_dir, "file2.txt")])

    def tearDown(self):
        if 'WFE_INPUT_JSON' in os.environ:
            del os.environ['WFE_INPUT_JSON']

if __name__ == '__main__':
    unittest.main()
