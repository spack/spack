from spack.pkg.builtin.scorep import Scorep as BuiltinScorep


class Scorep(BuiltinScorep):
    def configure_args(self):
        config_args = super().configure_args()
        # new hpe-mpi hmpt version is mpich abi compatible
        if self.spec.satisfies('^hpe-mpi'):
            config_args.append('--with-mpi=mpich3')
        return config_args
