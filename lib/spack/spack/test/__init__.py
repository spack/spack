import sys
import unittest
import spack

def run(test_name, verbose=False):
    __import__(__package__ + "." + test_name)

    # This just runs unittest.main on the module with the provided name
    test_module = getattr(spack.test, test_name)

    verbosity=1
    if verbose: verbosity = 2
    unittest.main(module=test_module, argv=sys.argv[:1], verbosity=verbosity)
