# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 01:10:34 2021

@author: User
"""

import requests


class Employee:
    """A sample Employee class"""

    def function(self):
        pass

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay


    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

