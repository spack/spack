import os

from spack import *


class Fleur(Package):
	"""FLEUR (Full-potential Linearised augmented plane wave in EURope)
       is a code family for calculating groundstate as well as excited-state properties
	   of solids within the context of density functional theory (DFT)."""

	homepage = "https://www.flapw.de/MaX-5.1"
	git = "https://iffgit.fz-juelich.de/fleur/fleur.git"

	version('MaX-R5.1', tag='MaX-R5.1')
	version('MaX-R5',	tag='MaX-R5')
	version('MaX-R4',	tag='MaX-R4')
	version('MaX-R3.1',	tag='MaX-R3.1')
	version('MaX-R3',	tag='MaX-R3')
	version('MaX-R2.1',	tag='MaX-R2.1')
	version('MaX-R2',	tag='MaX-R2')
	version('MaX-R2',	tag='MaX-R2')
	version('MaX-R1.3',	tag='MaX-R1.3')
	version('MaX-R1.2',	tag='MaX-R1.2')
	version('MaX-R1.1',	tag='MaX-R1.1')
	version('MaX-R1',	tag='MaX-R1')

	variant('mpi', default=True, description='Build with MPI support')
	variant('hdf5', default=False, description='Enable HDF5 support')
	variant('scalapack', default=False, description='Enable SCALAPACK')
	variant('elpa', default=False, description="Enable ELPA support")
	variant('magma', default=False, description='Enable Magma support')
	variant('libxc', default=False, description='Enable libxc support')
	variant('spfft', default=False, description='Enable spfft support')
	variant('wannier90', default=False, description='Enable wannier90 support')
	variant('openmp', default=False, description="Enable OpenMP support.")
	variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

	depends_on('blas')
	depends_on('lapack')
	depends_on('fftw-api')
	depends_on('libxml2')
	depends_on('cmake')
	depends_on('python')
	depends_on('mpi', when='+mpi')
	depends_on('scalapack', when='+scalapack')
	depends_on('libxc', when='+libxc')
	depends_on('hdf5+hl+fortran', when='+hdf5')
	depends_on('magma+fortran', when='+magma')
	depends_on('wannier90', when='+wannier90')
	depends_on('spfft+fortran', when='+spfft')
	depends_on('elpa', when='+elpa')

	phases = ['configure', 'build', 'install']

	conflicts('%intel@:16.0.4', 
		msg='Intel gfort<16.0 will most probably not work correctly')
	conflicts('%gcc@:6.3.0', 
		msg='gfortran is known to work with versions newer than 6.3.')
	conflicts('%pgi@:18.4.0', 
		msg='You need at least PGI version 18.4 but might still run into some problems.')
	conflicts('%python@:3.0.0', 
		msg='At least a Python3 is mandatory')
	conflicts('~scalapack', when='+elpa', msg='ELPA requires SCALAPACK support')

	def setup_build_environment(self, env):
		spec = self.spec

		if '+mpi' in spec:
			env.set('CC', spec['mpi'].mpicc, force=True)
			env.set('FC', spec['mpi'].mpifc, force=True)
			env.set('CXX', spec['mpi'].mpicxx, force=True)

	def configure(self, spec, prefix):
		spec = self.spec
		sh = which('sh')

		options = {
			"-link":[],
			"-libdir":[],
			"-includedir":[],
			#"-flags":[]
		}

		options["-link"].append(spec['blas'].libs.link_flags)
		options["-libdir"].append(spec['blas'].prefix.lib)
		options["-includedir"].append(spec['blas'].prefix.include)

		options["-link"].append(spec['lapack'].libs.link_flags)
		options["-libdir"].append(spec['lapack'].prefix.lib)
		options["-includedir"].append(spec['lapack'].prefix.include)

		options["-link"].append(spec['fftw'].libs.link_flags)
		options["-libdir"].append(spec['fftw'].prefix.lib)
		options["-includedir"].append(spec['fftw'].prefix.include)

		options["-link"].append(spec['libxml2'].libs.link_flags)
		options["-libdir"].append(spec['libxml2'].prefix.lib)
		options["-includedir"].append(spec['libxml2'].prefix.include)

		if '+scalapack' in spec:
			options["-link"].append(spec['scalapack'].libs.link_flags)
			options["-libdir"].append(spec['scalapack'].prefix.lib)
		if '+libxc' in spec:
			options["-link"].append(spec['libxc'].libs.link_flags)
			options["-libdir"].append(spec['libxc'].prefix.lib)
			options["-includedir"].append(spec['libxc'].prefix.include)
		if '+hdf5' in spec:
			options["-link"].append(spec['hdf5'].libs.link_flags)
			options["-libdir"].append(spec['hdf5'].prefix.lib)
			options["-includedir"].append(spec['hdf5'].prefix.include)
		if '+magma' in spec:
			options["-link"].append(spec['magma'].libs.link_flags)
			options["-libdir"].append(spec['magma'].prefix.lib)
			options["-includedir"].append(spec['magma'].prefix.include)
		if '+wannier90' in spec:
			# Workaround: The library is not called wannier90.a/so
			#	for this reason spec['wannier90'].libs.link_flags fails!
			options["-link"].append('-lwannier')
			options["-libdir"].append(spec['wannier90'].prefix.lib)
		if '+spfft' in spec:
			options["-link"].append(spec['spfft'].libs.link_flags)
			# Workaround: The library is installed in /lib64 not /lib
			options["-libdir"].append(spec['spfft'].prefix.lib+"64")
			# Workaround: The library needs spfft.mod in include/spfft path
			options["-includedir"].append(
				join_path(spec['spfft'].prefix.include, "spfft")
			)
		if '+elpa' in spec:
			options["-link"].append(spec['elpa'].libs.link_flags)
			options["-libdir"].append(spec['elpa'].prefix.lib)
			# Workaround: The library needs elpa.mod in include/elpa_%VERS/modules
			options["-includedir"].append(spec['elpa'].prefix.include)
			options["-includedir"].append(spec['elpa'].headers.include_flags[2:])
			options["-includedir"].append(
				join_path(spec['elpa'].headers.include_flags[2:], "modules")
			)
        
		args = []
		args.append("-link")
		args.append(" ".join(options["-link"]))
		args.append("-libdir")
		args.append(" ".join(options["-libdir"]))
		args.append("-includedir")
		args.append(" ".join(options["-includedir"]))
		#args.append("-flags")
		#args.append(" ".join(options["-flags"]))

		sh('configure.sh', *args)

	def build(self, spec, prefix):
		with working_dir('build'):
			make()

	def install(self, spec, prefix):
		with working_dir('build'):
			# copy bin
			mkdirp(prefix.bin)
			if '+mpi' in spec:
				install('fleur_MPI', prefix.bin)
			else:
				install('fleur', prefix.bin)
			install('inpgen', prefix.bin)

			# copy include
			mkdirp(prefix.include)
			install_tree('include', prefix.include)
