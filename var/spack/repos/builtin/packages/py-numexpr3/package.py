from spack import *


class PyNumexpr(PythonPackage):
    """Numexpr3 is a fast numerical expression evaluator for NumPy. With it,
    expressions that operate on arrays (like "3*a+4*b") are accelerated and
    use less memory than doing the same calculation in Python.
    In addition, its multi-threaded capabilities can make use of all your
    cores, which may accelerate computations, most specially if they are not
    memory-bounded (e.g. those using transcendental functions).
    Compared to NumExpr 2.6, functions have been re-written in a fashion such
    that gcc can auto-vectorize them with SIMD instruction sets such as
    SSE2 or AVX2, if your processor supports them. Use of a newer version of
    gcc such as 5.4 is strongly recommended."""
    homepage = "https://github.com/pydata/numexpr/tree/numexpr-3.0"
    url = "https://files.pythonhosted.org/packages/f2/fe/52b6aca524622e57fb1fa9681c6e12bf3dd7df42c93edc2900ae844d42ce/numexpr3-3.0.1a1.tar.gz"

    version('3.0.1.a1', '9fa8dc59b149aa1956fc755f982a78ad')
    # TODO: Add CMake build system for better control of passing flags related
    # to CPU ISA.

    depends_on('python@2.6:')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-setuptools@18.2:', type='build')
