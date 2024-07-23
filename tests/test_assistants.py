# ./tests/test_assistants.py
import unittest
from assistants.base_assistant import BaseAssistant

class TestBaseAssistant(unittest.TestCase):
    def test_respond(self):
        with self.assertRaises(NotImplementedError):
            BaseAssistant().respond('test')

if __name__ == '__main__':
    unittest.main()
