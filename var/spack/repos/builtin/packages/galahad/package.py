from spack import *
import os
import StringIO
import llnl.util.tty as tty
import shutil

# http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
def xcopytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

class Galahad(Package):
    """Optimization Library"""

    homepage = "http://www.galahad.rl.ac.uk/"

    # Galahad has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('2.60003', '2a0b77eacb55987118d2217a318f8541')
    url='http://none/galahad-2.60003.tar.gz'

    mainatiners = ['citibeth']

    # GALAHAD uses its own internal BLAS/LAPACK, I don't know how to turn it off for now
    # depends_on('blas')
    # depends_on('lapack')
    depends_on('gsl')

    depends_on('archdefs-src')
    depends_on('cutest-src')
    depends_on('sifdecode-src')

    def install(self, spec, prefix):
        stage = self.stage
        os.chdir(stage.source_path)

        try:
            shutil.rmtree('cutest')
        except:
            pass
        try:
            shutil.rmtree('sifdecode')
        except:
            pass
        shutil.copytree(spec['cutest-src'].prefix, 'cutest')
        shutil.copytree(spec['sifdecode-src'].prefix, 'sifdecode')

        svn = which('svn')
        
#svn checkout --username anonymous http://ccpforge.cse.rl.ac.uk/svn/cutest/archdefs/trunk ./archdefs
#svn checkout --username anonymous http://ccpforge.cse.rl.ac.uk/svn/cutest/sifdecode/trunk ./sifdecode
#svn checkout --username anonymous http://ccpforge.cse.rl.ac.uk/svn/cutest/cutest/trunk ./cutest

        #os.environ['BLAS'] = spec['blas'].prefix
        #os.environ['LAPACK'] = spec['lapack'].prefix
        os.environ['C_INCLUDE_PATH'] = os.path.join(spec['gsl'].prefix, 'include')
        os.environ['GALAHAD'] = spec.prefix
        os.environ['ARCHDEFS'] = spec['archdefs-src'].prefix
        os.environ['CUTEST'] = os.path.join(stage.source_path, 'cutest')
        os.environ['SIFDECODE'] = os.path.join(stage.source_path, 'sifdecode')

        with open('build_input.txt', 'w') as fout:
            fout.write('y3\nc\n6\n2\nn2\nn3\nnyydydy')
            fout.write('\n')

        install_optsuite = Executable(os.path.join(spec['archdefs-src'].prefix, 'install_optsuite'))
        with open('build_input.txt', 'r') as fin:
            try:
                install_optsuite(input=fin)
            except Exception as e:
                tty.warn('Ignoring error while building (this is normal): %s' % str(e))

        version = 'pc64.lnx.gfo'
        shutil.copytree(
            os.path.join(stage.source_path, 'modules', version, 'double'),
            os.path.join(spec.prefix, 'include'))
        xcopytree(
            os.path.join(stage.source_path, 'cutest', 'modules', version, 'double'),
            os.path.join(spec.prefix, 'include'))
        xcopytree(
            os.path.join(stage.source_path, 'sifdecode', 'objects', version, 'double'),
            os.path.join(spec.prefix, 'include'))

        shutil.copytree(
            os.path.join(stage.source_path, 'objects', version, 'double'),
            os.path.join(spec.prefix, 'lib'))

        xcopytree(
            os.path.join(stage.source_path, 'cutest', 'objects', version, 'double'),
            os.path.join(spec.prefix, 'lib'))

        xcopytree(
            os.path.join(stage.source_path, 'sifdecode', 'objects', version, 'double'),
            os.path.join(spec.prefix, 'lib'))
