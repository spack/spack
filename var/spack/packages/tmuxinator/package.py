from spack import *

class Tmuxinator(Package):
    """A session configuration creator and manager for tmux"""
    homepage = "https://github.com/tmuxinator/tmuxinator"
    url      = "https://github.com/tmuxinator/tmuxinator"

    version('0.6.11', 
        git='https://github.com/tmuxinator/tmuxinator',
        tag='v0.6.11')

    extends('ruby')

    def install(self, spec, prefix):
      gem('build', 'tmuxinator.gemspec')
      gem('install', 'tmuxinator-{}.gem'.format(self.version))

