import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apeer_dev_kit import _core

class TestsCore(unittest.TestCase):

    def test_init_givenNoEnvironmentVariable_coreIsNotInitialized(self):
        with self.assertRaises(KeyError):
            _core._core()

    def test_init_givenEmptyInputJson_coreIsInitialized(self):
        os.environ["WFE_INPUT_JSON"] = "{}"

        core = _core._core()

        self.assertTrue(core)
        self.assertEqual(core._wfe_output_params_file, "")
        self.assertEqual(core._outputs, {})

    def test_init_givenInputJson_coreIsInitalized(self):
        os.environ["WFE_INPUT_JSON"] = '{"WFE_output_params_file":"param.json","red":0.2,"input_image":"test.jpg"}'

        core = _core._core()

        self.assertTrue(core)
        self.assertEqual(core._input_json["WFE_output_params_file"], "param.json")
    
    def test_get_inputs_givenNoParamFileKey_throwsKeyErrorException(self):
        os.environ["WFE_INPUT_JSON"] = '{"red":0.2,"input_image":"test.jpg"}'
        core = _core._core()

        with self.assertRaises(KeyError):
            core._get_inputs()

    def test_get_inputs_givenInputJson_paramFileIsNotPartOfInputs(self):
        os.environ["WFE_INPUT_JSON"] = '{"WFE_output_params_file":"param.json","red":0.2}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertFalse('WFE_output_params_file' in inputs)
        self.assertEqual(len(inputs), 1)

    def test_get_inputs_givenDecimal_isDeserialized(self):
        os.environ["WFE_INPUT_JSON"] = '{"WFE_output_params_file":"param.json","red":0.2}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs["red"], 0.2)

    def test_get_inputs_givenInteger_isDeserialized(self):
        os.environ["WFE_INPUT_JSON"] = '{"WFE_output_params_file":"param.json","red":2}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs["red"], 2)

    def test_get_inputs_givenString_isDeserialized(self):
        os.environ["WFE_INPUT_JSON"] = '{"WFE_output_params_file":"param.json","value":"testValue"}'
        core = _core._core()

        inputs = core._get_inputs()
        
        self.assertEqual(inputs["value"], "testValue")

    def tearDown(self):
        if "WFE_INPUT_JSON" in os.environ:
            del os.environ['WFE_INPUT_JSON']

if __name__ == '__main__':
    unittest.main()
