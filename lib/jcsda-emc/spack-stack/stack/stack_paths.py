import spack
import os

# Hidden file in top-level spack-stack dir so this module can
# find relative config files. Assuming Spack is a submodule of
# spack-stack.
check_file = '.spackstack'


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, check_file)):
        raise Exception('Not a submodule of spack-stack')

    return os.path.join(stack_dir, *paths)


site_path = stack_path('configs', 'sites')
app_path = stack_path('configs', 'apps')
container_path = stack_path('configs', 'containers')
