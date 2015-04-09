from spack import *

class Qhull(Package):
    """Qhull computes the convex hull, Delaunay triangulation, Voronoi
       diagram, halfspace intersection about a point, furt hest-site
       Delaunay triangulation, and furthest-site Voronoi diagram. The
       source code runs in 2-d, 3-d, 4-d, and higher dimensions. Qhull
       implements the Quickhull algorithm for computing the convex
       hull. It handles roundoff errors from floating point
       arithmetic. It computes volumes, surface areas, and
       approximations to the convex hull.

       Qhull does not support triangulation of non-convex surfaces,
       mesh generation of non-convex objects, medium-sized inputs in
       9-D and higher, alpha shapes, weighted Voronoi diagrams,
       Voronoi volumes, or constrained Delaunay triangulations."""

    homepage = "http://www.qhull.org"

    version('1.0', 'd0f978c0d8dfb2e919caefa56ea2953c',
            url="http://www.qhull.org/download/qhull-2012.1-src.tgz")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
