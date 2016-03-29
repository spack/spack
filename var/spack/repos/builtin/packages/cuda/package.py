from spack import *
from glob import glob
import os

class Cuda(Package):
    """CUDA is a parallel computing platform and programming model invented by
    NVIDIA. It enables dramatic increases in computing performance by harnessing
    the power of the graphics processing unit (GPU).

    Note: NVIDIA does not provide a download URL for CUDA so you will need to
    download it yourself. Go to https://developer.nvidia.com/cuda-downloads
    and select your Operating System, Architecture, Distribution, and Version.
    For the Installer Type, select runfile and click Download. Spack will search
    your current directory for this file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a mirror,
    see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "http://www.nvidia.com/object/cuda_home_new.html"
    url      = "file://%s/cuda_7.5.18_linux.run" % os.getcwd()

    version('7.5.18', '4b3bcecf0dfc35928a0898793cf3e4c6', expand=False)

    def install(self, spec, prefix):
        runfile = glob(os.path.join(self.stage.path, 'cuda*.run'))[0]
        chmod = which('chmod')
        chmod('+x', runfile)
        runfile = which(runfile)

        # Note: NVIDIA does not officially support many newer versions of compilers.
        # For example, on CentOS 6, you must use GCC 4.4.7 or older.
        # The --override flag disables these checks. See:
        # http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#system-requirements
        # for details.

        runfile(
            '--silent',   # disable interactive prompts
            '--verbose',  # create verbose log file
            '--override', # ignore compiler checks
            '--toolkit',  # install CUDA Toolkit
            '--toolkitpath=%s' % prefix
        )

