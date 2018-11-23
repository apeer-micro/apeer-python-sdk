import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apeer_dev_kit import core

class TestsCore(unittest.TestCase):

    def test_coreIsInitialized(self):
        _core = core.core()
        self.assertTrue(_core)
        self.assertEqual(_core._wfe_output_params_file, "")
        self.assertEqual(_core._outputs, {})

if __name__ == '__main__':
    unittest.main()