from spack import *
from spack.pkg.builtin.stat import Stat as BuiltinStat


class Stat(BuiltinStat):
    __doc__ = BuiltinStat.__doc__

    # That commit is 4.1.0 + a bunch of fixes, PYTHONPATH handling incuded
    version('4.1.0-2021-12-02', commit='ff48de751f7716133cfb95a912ee8787da9acbeb')

    depends_on('py-xdot@1.0', type=('build', 'run'), when='@4.0.1: +gui')

    patch('fix-pango.patch', when='@4.1.0:')

    def setup_run_environment(self, env):
        for d in self.spec.traverse(deptype=('run',), root=True):
            python = self.spec['python']
            if d.package.extends(python):
                env.prepend_path('PYTHONPATH', join_path(
                    d.prefix, python.package.site_packages_dir))
