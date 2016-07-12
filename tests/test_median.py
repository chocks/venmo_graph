import unittest
import filecmp
from src.find_median import Median


class MedianTestCase(unittest.TestCase):

    def test_median_calc1(self):
        median = Median()
        median.find_median(input_file="../venmo_input/sample1.txt", output_file="../venmo_output/output.txt")
        isFileExists = "../venmo_output/output.txt"
        self.assertTrue(isFileExists)

        stat = filecmp.cmp("../venmo_output/output.txt", "../artifacts/output1.txt")
        self.assertTrue(stat)

    def test_median_calc2(self):
        median = Median()
        median.find_median(input_file="../venmo_input/sample2.txt", output_file="../venmo_output/output.txt")
        isFileExists = "../venmo_output/output.txt"
        self.assertTrue(isFileExists)

        stat = filecmp.cmp("../venmo_output/output.txt", "../artifacts/output2.txt")
        self.assertTrue(stat)

    def test_median_calc3(self):
        median = Median()
        median.find_median(input_file="../venmo_input/sample3.txt", output_file="../venmo_output/output.txt")
        isFileExists = "../venmo_output/output.txt"
        self.assertTrue(isFileExists)

        stat = filecmp.cmp("../venmo_output/output.txt", "../artifacts/output3.txt")
        self.assertTrue(stat)

    def test_median_calc4(self):
        median = Median()
        median.find_median(input_file="../venmo_input/sample4.txt", output_file="../venmo_output/output.txt")
        isFileExists = "../venmo_output/output.txt"
        self.assertTrue(isFileExists)

        stat = filecmp.cmp("../venmo_output/output.txt", "../artifacts/output4.txt")
        self.assertTrue(stat)

    def test_median_calc5(self):
        median = Median()
        median.find_median(input_file="../venmo_input/venmo-trans.txt", output_file="../venmo_output/output.txt")
        isFileExists = "../venmo_output/output.txt"
        self.assertTrue(isFileExists)

        stat = filecmp.cmp("../venmo_output/output.txt", "../artifacts/output.txt")
        self.assertTrue(stat)

if __name__ == '__main__':
    unittest.main()
