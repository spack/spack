import re
from spack.architecture import OperatingSystem


class LinuxDistro(OperatingSystem):
    """ This class will represent the autodetected operating system
        for a Linux System. Since there are many different flavors of
        Linux, this class will attempt to encompass them all through
        autodetection using the python module platform and the method
        platform.dist()
    """

    def __init__(self):
        try:
            # This will throw an error if imported on a non-Linux platform.
            from external.distro import linux_distribution
            distname, version, _ = linux_distribution(
                full_distribution_name=False)
            distname, version = str(distname), str(version)
        except ImportError as e:
            distname, version = 'unknown', ''

        # Grabs major version from tuple on redhat; on other platforms
        # grab the first legal identifier in the version field.  On
        # debian you get things like 'wheezy/sid'; sid means unstable.
        # We just record 'wheezy' and don't get quite so detailed.
        version = re.split(r'[^\w-]', version)[0]

        super(LinuxDistro, self).__init__(distname, version)
