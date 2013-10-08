import unittest
import spack.spec


class ConcretizeTest(unittest.TestCase):

    def check_concretize(self, abstract_spec):
        abstract = spack.spec.parse_one(abstract_spec)
        self.assertTrue(abstract.concretized().concrete)


    def test_packages(self):
        self.check_concretize("libelf")
