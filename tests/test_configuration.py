from unittest import TestCase
from kubehelm.core.configuration import Configuration, CONFIG


class TestConfiguration(TestCase):

    def test_default_config(self):
        self.assertEqual(CONFIG.get('debug'), "true")
        self.assertEqual(CONFIG.getboolean('debug'), True)

    def test_update_config_file(self):
        config = Configuration().update_config_file("test1", "123")
        self.assertEqual(config.get("test1"), "123")
        self.assertEqual(CONFIG.getboolean('debug'), True)

        config = Configuration().update_config_file("test2", "456")
        self.assertEqual(config.get("test2"), "456")

        config = Configuration().update_config_file("test3", "789")
        self.assertEqual(config.getint("test1"), 123)
        self.assertEqual(config.getint("test2"), 456)
        self.assertEqual(config.getint("test3"), 789)

        self.assertEqual(config.get('debug'), "true")
        self.assertEqual(config.getboolean('debug'), True)
