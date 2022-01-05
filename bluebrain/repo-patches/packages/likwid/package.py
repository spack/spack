from spack import *
from spack.pkg.builtin.likwid import Likwid as BuiltinLikwid


class Likwid(BuiltinLikwid):
    variant('setgid', default=False, description='enable setgid flag '
            + 'for likwid-accessD and change its group to LIWKID_GROUP. '
            + 'Note: set LIWKID_GROUP env variable')

    conflicts('+setgid', when='@:4.0.1')  # accessD was added in 4.1

    supported_compilers = {'clang': 'CLANG', 'gcc': 'GCC', 'intel': 'ICC'}

    @run_after('install')
    def change_group(self):
        accessD = join_path(self.prefix.sbin, 'likwid-accessD')
        if self.spec.satisfies('+setgid'):
            likwid_group = 'likwid'
            if 'LIKWID_GROUP' in os.environ:
                likwid_group = os.environ['LIKWID_GROUP']
            chgrp = which('chgrp')
            chmod = which('chmod')
            chgrp(likwid_group, accessD)
            chmod('g+s', accessD)
