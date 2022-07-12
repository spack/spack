import os

import pytest

import spack
import spack.main

stack_create = spack.main.SpackCommand('stack')


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, '.spackstack')):
        return None

    return os.path.join(stack_dir, *paths)


test_dir = stack_path('envs', 'unit-tests', 'stack-create')


def all_templates():
    template_path = stack_path('configs', 'templates')
    if template_path:
        _, templates, _ = next(os.walk(template_path))
        return list(templates)
    else:
        return None


def all_sites():
    site_path = stack_path('configs', 'sites')
    if site_path:
        _, sites, _ = next(os.walk(site_path))
        return list(sites)
    else:
        return None


def all_containers():
    container_path = stack_path('configs', 'containers')
    if container_path:
        _, _, containers = next(os.walk(container_path))
        return containers
    else:
        return None


@pytest.mark.extension('stack')
@pytest.mark.parametrize('template', all_templates())
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_apps(template):
    if not template:
        return
    stack_create('create', 'env', '--template', template,
                 '--dir', test_dir, '--overwrite')


@pytest.mark.extension('stack')
@pytest.mark.parametrize('site', all_sites())
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_sites(site):
    if not site:
        return
    stack_create('create', 'env', '--site', site,
                 '--dir', test_dir, '--overwrite')


@pytest.mark.extension('stack')
@pytest.mark.parametrize('container', all_containers())
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_containers(container):
    if not container:
        return
    container_wo_ext = os.path.splitext(container)[0]
    stack_create('create', 'ctr', container_wo_ext,
                 '--dir', test_dir, '--overwrite')
