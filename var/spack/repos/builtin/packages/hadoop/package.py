from spack import *

import distutils
from distutils import dir_util


class Hadoop(Package):
    """
    The Apache Hadoop software library is a framework that
    allows for the distributed processing of large data sets
    across clusters of computers using simple programming models.
    """

    homepage = "http://hadoop.apache.org/"
    url      = "http://hadoop.apache.org/releases.html"

    version('2.6.4', '37019f13d7dcd819727be158440b9442',
            url = 'http://mirrors.ocf.berkeley.edu/apache/hadoop/common/hadoop-2.6.4/hadoop-2.6.4.tar.gz')

    depends_on('jdk')

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree('.', prefix)
