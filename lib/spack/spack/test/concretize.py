import unittest
from spack.spec import Spec


class ConcretizeTest(unittest.TestCase):

    def check_concretize(self, abstract_spec):
        abstract = Spec(abstract_spec)
        print abstract
        print abstract.concretized()
        print abstract.concretized().concrete
        self.assertTrue(abstract.concretized().concrete)


    def test_packages(self):
        pass
        #self.check_concretize("libelf")
