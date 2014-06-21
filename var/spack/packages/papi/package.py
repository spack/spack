from spack import *
import os

class Papi(Package):
    """PAPI provides the tool designer and application engineer with a consistent interface and methodology for use of the performance counter hardware found in most major microprocessors. PAPI enables software engineers to see, in near real time, the relation between software performance and processor events.
    In addition Component PAPI provides access to a collection of components that expose performance measurement opportunites across the hardware and software stack."""
    homepage = "http://icl.cs.utk.edu/papi/index.html"
    url      = "http://icl.cs.utk.edu/projects/papi/downloads/papi-5.3.0.tar.gz"

    versions = { '5.3.0' : '367961dd0ab426e5ae367c2713924ffb', }

    def install(self, spec, prefix):
        os.chdir("src/")

        configure_args=["--prefix=%s" % prefix]

		# need to force consistency in the use of compilers
        if spec.satisfies('%gcc'):
            configure_args.append('CC=gcc')
            configure_args.append('MPICH_CC=gcc')
        if spec.satisfies('%intel'):
            configure_args.append('CC=icc')
            configure_args.append('MPICH_CC=icc')

        configure(*configure_args)

        make()
        make("install")

