from spack import *
import os

class Papi(Package):
    """PAPI provides the tool designer and application engineer with a
       consistent interface and methodology for use of the performance
       counter hardware found in most major microprocessors. PAPI
       enables software engineers to see, in near real time, the
       relation between software performance and processor events.  In
       addition Component PAPI provides access to a collection of
       components that expose performance measurement opportunites
       across the hardware and software stack."""
    homepage = "http://icl.cs.utk.edu/papi/index.html"

    url      = "http://icl.cs.utk.edu/projects/papi/downloads/papi-5.4.1.tar.gz"
    version('5.4.1', '9134a99219c79767a11463a76b0b01a2')
    version('5.3.0', '367961dd0ab426e5ae367c2713924ffb')

    def install(self, spec, prefix):
        os.chdir("src/")

        configure_args=["--prefix=%s" % prefix]

        # PAPI uses MPI if MPI is present; since we don't require an
        # MPI package, we ensure that all attempts to use MPI fail, so
        # that PAPI does not get confused
        configure_args.append('MPICC=:')

        configure(*configure_args)

        make()
        make("install")

