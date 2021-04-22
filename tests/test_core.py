from unittest import TestCase


class TestOne(TestCase):
    def setUp(self):
        pass
        # self.fish_tank = FishTank()

    def test_one(self):
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            raise ValueError("my text")
        self.assertEqual(str(exception_context.exception), "my text")
