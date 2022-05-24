import pytest
import spack.main
import os
import spack
import spack.environment as ev

stack_create = spack.main.SpackCommand('stack')


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, '.spackstack')):
        raise Exception('Not a submodule of spack-stack')

    return os.path.join(stack_dir, *paths)


test_dir = stack_path('envs', 'unit-tests', 'setup-meta-modules')

@pytest.mark.extension('stack')
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_setup_meta_modules():
    os.makedirs(test_dir, exist_ok=True)

    env_dir = os.path.join(test_dir)
    create_output = stack_create('create', 'env', '--dir', env_dir,
                                 '--app', 'empty', '--site', 'default', '--overwrite')

    # Create empty env
    env_dir = os.path.join(env_dir, 'empty.default')
    env = ev.Environment(path=env_dir, init_file=os.path.join(env_dir, 'spack.yaml'))
    ev.activate(env)

    comp = 'gcc'
    comp_ver = '9.4.0'
    mpi = 'openmpi'
    mpi_ver = '4.0.1'
    module_dir = os.path.join(env_dir, 'install', 'modulefiles')
    compiler_module_path = os.path.join(module_dir, comp, comp_ver)
    mpi_module_path = os.path.join(module_dir, mpi, mpi_ver, comp, comp_ver)

    # Setup env and pretend that a build exists
    # by creating the module directory structure.
    scope = env.env_file_config_scope_name()
    spack.config.add('packages:all:compiler:[{}]'.format(comp), scope=scope)
    spack.config.add('packages:all:providers:mpi:[{}]'.format(mpi), scope=scope)
    spack.main.SpackCommand('stack')
    os.makedirs(compiler_module_path)
    os.makedirs(mpi_module_path)
    cmd = spack.main.SpackCommand('external')
    output = cmd('find', 'python')
    with env.write_transaction():
        env.write()
    meta_module_output = stack_create('setup-meta-modules')
