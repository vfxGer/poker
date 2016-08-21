'''
Created on 29 Apr 2012

@author: gkeating
'''
import unittest
import mock

import os

from poker_core import randomnumbers

class RandomNumberTest(unittest.TestCase):
    @mock.patch('time.time')
    def test_getRandomSeed(self, mockTime):
        mockTime.return_value = 1335696322.6
        randomnumbers.getRandomSeed()

    def test_pickle_path(self):
        self.assertTrue(os.path.exists(randomnumbers.pickle_path()))
def main():
    unittest.main()
if __name__=="__main__":
    main()