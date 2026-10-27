
import unittest
from src.main import main


class TestSetup(unittest.TestCase):

    def test_main_runs(self):
        main()


if __name__ == "__main__":
    unittest.main()
