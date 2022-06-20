from parameterized import parameterized
import unittest
import json
from CaesarShift import ShiftString


# --> RUN CMD: 'py UnitTests.py -v

testCasesFile = "ShiftTestCases.json"

def testCasesList():
    # If the keys of all the testcases are in the same order, I would do the following to obtain the list:
        # testCasesList = [list(testCase.values()) for testCase in json.load(open(testCasesFile))]
    # However, to handle potential inconsistencies in the order of data (key+value) in ShiftTestCases.json, I order the keys first
        # strangely; 'test_shiftString(self,.. ) expects the message 'msg' to be first. If the message is elsewhere and the assertEqual() is constructed correctly,
        # the testcase will PASS but the displayed message is the first given parameter. Passing an other msg in self.assertEqual() doesn't change anything. 
        # Therefor, 'name' was changed to 'a_name' as a key in the json file to be the first key in the sorted list.
    testCases = json.load(open(testCasesFile))
    sortedKeys = sorted(testCases[0].keys())
    # nested listcomprehension to create a list of lists of the test-case data
    testCasesList = [[testCase.get(key) for key in sortedKeys] for testCase in testCases]
    return testCasesList

class TestCases(unittest.TestCase):
    # alternatively to subTest() of the unittest framework I use @parametirzed.
    # this enables me to print and count all subtests separately, where subTests() only counted 1 test
    @parameterized.expand(testCasesList)
    def test_shiftString(self, msg, expected, input, shift ):
        #print(msg)
        self.assertEqual(ShiftString(shift, input), expected)


if __name__ == '__main__':
    unittest.main()