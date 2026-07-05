import unittest
from unittest.mock import Mock, patch

from lib import cloud_config


class CloudConfigTests(unittest.TestCase):
    def test_default_demo_mode_is_on_when_secret_is_missing(self):
        with patch.object(cloud_config, "st") as fake_st:
            fake_st.secrets.get.side_effect = FileNotFoundError("no secrets")

            self.assertTrue(cloud_config.default_demo_mode())

    def test_default_demo_mode_can_be_disabled_by_secret(self):
        with patch.object(cloud_config, "st") as fake_st:
            fake_st.secrets = Mock()
            fake_st.secrets.get.return_value = "false"

            self.assertFalse(cloud_config.default_demo_mode())


if __name__ == "__main__":
    unittest.main()
