import unittest

from resources.items import validate_token


class TestValidation(unittest.TestCase):

    def test_present(self):
        x, y, z = validate_token({'token': '1234'})
        self.assertEqual('1234', x)

    def test_throws_on_absent_value(self):
        x, y, z = validate_token({'xxx': '1234'})
        self.assertFalse(x)
        self.assertEqual(z, 400)
        self.assertEqual(y['message'], 'The token cannot be left blank!')


if __name__ == '__main__':
    unittest.main()
