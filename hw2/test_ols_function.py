# -*- coding: utf-8 -*-

import unittest
from ols_function import linear_regression as lr
import numpy as np



class TestOLS(unittest.TestCase):
       
    # checks if given inputs are both array
    def test_Type(self):
        X = None
        Y = 0
        self.assertRaises(ValueError, lr, X, Y)
    
    # checks if X has at least 3 variables the including conrol variable and ones for y-intercept
    # checks if Y has at most 1 variable
    def test_RowColumn(self):
        X = np.random.randint(5, size=(134, 2))
        Y = np.random.randint(5, size=(134, 2))
        self.assertRaises(ValueError, lr, X, Y)
    
    # checks if X.T can be multiplied with Y
    def test_MatrixMult(self):
        X = np.random.randint(5, size=(134, 4))
        Y = np.random.randint(5, size=(200, 1))
        self.assertRaises(ValueError, lr, X, Y)
    
    # checks if given input arrays have non-numeric values
    def test_NonNumeric(self):
        X = np.array([[4, 2], [3, 2], [1, 0], [3, "f"]])
        Y = np.array([[2], [0], [4], [1]])
        self.assertRaises(AttributeError, lr, X, Y)
        self.assertRaises(AttributeError, lr, X, Y)
        
    #check for underdetermined system
    def test_Other(self):
        X = np.random.randint(5, size=(3, 4))
        Y = np.random.randint(5, size=(3, 1))
        self.assertRaises(AttributeError, lr, X, Y)
        


if __name__ == '__main__':
    unittest.main()

