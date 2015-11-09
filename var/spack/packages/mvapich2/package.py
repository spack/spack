from spack import *


class Mvapich2(Package):
    """MVAPICH2 is an MPI implementation for Infiniband networks."""
    homepage = "http://mvapich.cse.ohio-state.edu/"

    version('2.2a', 'b8ceb4fc5f5a97add9b3ff1b9cbe39d2',
            url='http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2a.tar.gz')

    version('2.0', '9fbb68a4111a8b6338e476dc657388b4',
            url='http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.0.tar.gz')

    version('1.9', '5dc58ed08fd3142c260b70fe297e127c',
            url="http://mvapich.cse.ohio-state.edu/download/mvapich2/mv2/mvapich2-1.9.tgz")
    patch('ad_lustre_rwcontig_open_source.patch', when='@1.9')

    provides('mpi@:2.2', when='@1.9')  # MVAPICH2-1.9 supports MPI 2.2
    provides('mpi@:3.0', when='@2.0:')  # MVAPICH2-2.0 supports MPI 3.0

    variant('debug', default=False, description='Enables debug information and error messages at run-time')

    ##########
    # TODO : Process managers should be grouped into the same variant, as soon as variant capabilities will be extended
    # See https://groups.google.com/forum/#!topic/spack/F8-f8B4_0so
    variant('slurm', default=False, description='Sets slurm as the only process manager')
    variant('hydra', default=False, description='Sets hydra as one of the process managers')
    variant('gforker', default=False, description='Sets gforker as one of the process managers')
    variant('remshell', default=False, description='Sets remshell as one of the process managers')
    ##########

    # FIXME: those variants are mutually exclusive. A variant enum would fit here.
    variant('psm', default=False, description='Configures a build for QLogic PSM-CH3')
    variant('sock', default=False, description='Configures a build for TCP/IP-CH3')
    # TODO : a lot of network variants are still missing.
    # See http://mvapich.cse.ohio-state.edu/static/media/mvapich/mvapich2-2.0-userguide.html

    def set_build_type_flags(self, spec, configure_args):
        """
        Appends to configure_args the flags that depends only on the build type (i.e. release or debug)

        :param spec: spec
        :param configure_args: list of current configure arguments
        """
        if '+debug' in spec:
            build_type_options = [
                "--disable-fast",
                "--enable-error-checking=runtime",
                "--enable-error-messages=all"
            ]
        else:
            build_type_options = ["--enable-fast=all"]

        configure_args.extend(build_type_options)

    def set_process_manager(self, spec, configure_args):
        """
        Appends to configure_args the flags that will enable the appropriate process managers

        :param spec: spec
        :param configure_args: list of current configure arguments
        """
        # Check that slurm variant is not activated together with other pm variants
        has_slurm_incompatible_variant = any((x in spec for x in ['+hydra', '+gforker', '+remshell']))
        if '+slurm' in spec and has_slurm_incompatible_variant:
            raise RuntimeError(" %s : 'slurm' cannot be activated together with other process managers" % self.name)

        process_manager_options = []
        if '+slurm' in spec:
            process_manager_options = [
                "--with-pm=slurm"
            ]
        elif has_slurm_incompatible_variant:
            pm = []
            if '+hydra' in spec:
                pm.append('hydra')
            if '+gforker' in spec:
                pm.append('gforker')
            if '+remshell' in spec:
                pm.append('remshell')

            process_manager_options = [
                "--with-pm=%s" % ':'.join(pm)
            ]
        configure_args.extend(process_manager_options)

    def set_network_type(self, spec, configure_args):
        # Check that at most one variant has been activated
        # FIXME : ugly, as it does not scale at all (and is full of conditionals)
        count = 0
        if '+psm' in spec:
            count += 1
        if '+sock' in spec:
            count += 1
        if count > 1:
            raise RuntimeError('MVAPICH2 variants are mutually exclusive : only one can be selected at a time')

        # From here on I can suppose that ony one variant has been selected
        if '+psm' in spec:
            network_options = ["--with-device=ch3:psm"]
        elif '+sock' in spec:
            network_options = ["--with-device=ch3:sock"]
        else:
            network_options = ["--with-device=ch3:mrail", "--with-rdma=gen2"]

        configure_args.extend(network_options)

    def install(self, spec, prefix):
        # we'll set different configure flags depending on our environment
        configure_args = [
            "--prefix=%s" % prefix,
            "--enable-shared",
            "--enable-romio",
            "--disable-silent-rules",
            "--enable-debuginfo",
            "--enable-g=dbg"
        ]
        if not self.compiler.f77 and not self.compiler.fc:
            configure_args.append("--enable-fortran=none")

        # Set flags that depend only on the type of the build (debug, release)
        self.set_build_type_flags(spec, configure_args)
        # Set the process manager
        self.set_process_manager(spec, configure_args)
        # Determine network type by variant
        self.set_network_type(spec, configure_args)

        configure(*configure_args)
        make()
        make("install")
