""" Test checks if the architecture class is created correctly and also that
    the functions are looking for the correct architecture name
"""
import unittest
import spack
from spack.architecture import *

class ArchitectureTest(unittest.TestCase):

    def test_Architecture_class(self):
        a = Architecture('Cray-XC40')
        a.add_arch_strategy()
        self.assertEquals(a.get_arch_dict(), {'Cray-XC40': 'MODULES'})

    def test_get_sys_type_from_config_file(self):
        output_arch_class = get_sys_type_from_config_file()
        my_arch_class = Architecture('Linux x86_64','Cray-xc40')

        self.assertEqual(output_arch_class, my_arch_class)
