from spack import *

class Ppl(Package):
    """The Parma Polyhedra Library (PPL) provides numerical
    abstractions especially targeted at applications in the field of
    analysis and verification of complex systems. These abstractions
    include convex polyhedra, some special classes of polyhedra shapes
    that offer interesting complexity/precision tradeoffs, and grids
    which represent regularly spaced points that satisfy a set of
    linear congruence relations. The library also supports finite
    powersets and products of polyhedra and grids, a mixed integer
    linear programming problem solver using an exact-arithmetic
    version of the simplex algorithm, a parametric integer programming
    solver, and primitives for termination analysis via the automatic
    synthesis of linear ranking functions."""

    homepage = "http://bugseng.com/products/ppl/"
    url      = "http://bugseng.com/products/ppl/download/ftp/releases/1.1/ppl-1.1.tar.gz"

    version('1.1', '4f2422c0ef3f409707af32108deb30a7')

    depends_on("gmp")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-gmp=%s" % spec['gmp'].prefix)
        make()
        make("install")
