import re

from spack import *
from spack.pkg.builtin.intel import Intel as BuiltinIntel


class Intel(BuiltinIntel):
    def setup_run_environment(self, env):
        super(Intel, self).setup_run_environment(env)
        forbidden = re.compile(r'/(mpi|tbb)(/|$)')
        survivors = []
        for e in env.env_modifications:
            if 'MPI_' in e.name:
                continue
            elif 'PATH' in e.name or 'ROOT' in e.name:
                paths = [v for v in e.value.split(':')
                         if not forbidden.search(v)]
                if paths:
                    new_value = ':'.join(paths)
                    if new_value != e.value:
                        rejected = [v for v in e.value.split(':')
                                    if forbidden.search(v)]
                        for p in rejected:
                            print('-', p)
                    e.value = new_value
                    survivors.append(e)
            else:
                survivors.append(e)
        env.env_modifications = survivors
