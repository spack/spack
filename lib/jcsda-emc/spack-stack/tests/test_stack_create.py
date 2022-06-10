import pytest
import spack.main
import os
import spack

stack_create = spack.main.SpackCommand('stack')


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, '.spackstack')):
        raise Exception('Not a submodule of spack-stack')

    return os.path.join(stack_dir, *paths)


test_dir = stack_path('envs', 'unit-tests', 'stack-create')


def all_templates():
    _, templates, _ = next(os.walk(stack_path('configs', 'templates')))
    return list(templates)


def all_sites():
    _, sites, _ = next(os.walk(stack_path('configs', 'sites')))
    return list(sites)


def all_containers():
    _, _, containers = next(os.walk(stack_path('configs', 'containers')))
    return containers


#def all_specs():
#    bundles_dir = os.path.join(spack.paths.var_path, 'repos',
#                               'jcsda-emc-bundles', 'packages')
#    _, bundle_envs, _ = next(os.walk(bundles_dir))
#    return bundle_envs


@pytest.mark.extension('stack')
@pytest.mark.parametrize('template', all_templates())
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_apps(template):
    output = stack_create('create', 'env', '--template', template,
                          '--dir', test_dir, '--overwrite')


@pytest.mark.extension('stack')
@pytest.mark.parametrize('site', all_sites())
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_sites(site):
    output = stack_create('create', 'env', '--site', site,
                          '--dir', test_dir, '--overwrite')


#@pytest.mark.extension('stack')
#@pytest.mark.parametrize('spec', all_specs())
#@pytest.mark.filterwarnings('ignore::UserWarning')
#def test_specs(spec):
#    output = stack_create('create', 'env', '--specs', spec,
#                          '--dir', test_dir, '--overwrite')


@pytest.mark.extension('stack')
@pytest.mark.parametrize('container', all_containers())
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_containers(container):
    container_wo_ext = os.path.splitext(container)[0]
    output = stack_create('create', 'ctr', container_wo_ext,
                          '--dir', test_dir, '--overwrite')
