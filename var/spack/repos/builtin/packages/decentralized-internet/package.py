from spack import *


class DecentralizedInternet(Package):
    """A library for building decentralized and grid computing projects"""
    homepage = "https://lonero.readthedocs.io"
    url      = "https://github.com/Lonero-Team/Decentralized-Internet/releases/download/4.2.3/Decentralized.Internet.tar.bz2"
    maintainers = ['Lonero-Team', 'Mentors4edu']
    version('4.2.3', sha256='fb78c56fbebed12867e97c81e1ba61d5d5f85da4eb9925a8e740af89ff104ff3')

    def install(self, spec, prefix):
        make()
        make('install')
