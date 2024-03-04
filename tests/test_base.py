"""Base module tests for a4s_sealer_module."""

import unittest


class TestModule_Base(unittest.TestCase):
    """Base test class for a4s_sealer_module."""

    pass


class TestImports(TestModule_Base):
    """Test the imports of the module are working correctly"""

    def test_driver_import(self):
        """Test the driver and rest node imports"""
        import a4s_sealer_driver
        import a4s_sealer_rest_node

        assert a4s_sealer_driver
        assert a4s_sealer_rest_node


if __name__ == "__main__":
    unittest.main()
