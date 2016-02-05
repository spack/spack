from spack import *

class Qhull(Package):
    """Qhull computes the convex hull, Delaunay triangulation, Voronoi
       diagram, halfspace intersection about a point, furt hest-site
       Delaunay triangulation, and furthest-site Voronoi diagram. The
       source code runs in 2-d, 3-d, 4-d, and higher dimensions. Qhull
       implements the Quickhull algorithm for computing the convex
       hull. It handles roundoff errors from floating point
       arithmetic. It computes volumes, surface areas, and
       approximations to the convex hull."""

    homepage = "http://www.qhull.org"

    version('7.2.0', 'e6270733a826a6a7c32b796e005ec3dc',
            url="http://www.qhull.org/download/qhull-2015-src-7.2.0.tgz")

    version('1.0', 'd0f978c0d8dfb2e919caefa56ea2953c',
            url="http://www.qhull.org/download/qhull-2012.1-src.tgz")

    # https://github.com/qhull/qhull/pull/5
    patch('qhull-iterator.patch', when='@1.0')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
