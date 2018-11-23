import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apeer_dev_kit import _core

class TestsCore(unittest.TestCase):

    def setUp(self):
        os.environ["WFE_INPUT_JSON"] = "{}"

    def test_coreIsInitialized(self):
        core = _core._core()
        self.assertTrue(core)
        self.assertEqual(core._wfe_output_params_file, "")
        self.assertEqual(core._outputs, {})

if __name__ == '__main__':
    unittest.main()