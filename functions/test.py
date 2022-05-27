import sys
# from challenge_ioet.functions.functions_ioet import *
import unittest
# from functions.functions_ioet import *
sys.path.append("../")
from functions import create_dictGeneral

class Test_create_dict_general(unittest.TestCase):
    def create_dict_general_from_test_file(self):
        dict1={'LUIS':{'MO':'11:00-12:00','TH':'13:00-15:00','SU':'10:00-15:00'}}
        dict_general=create_dictGeneral("files_acme/acme2.txt")
        self.assertEqual(dict1,dict_general,'Deben ser igual')


if __name__=='__main__':
    unittest.main()    
