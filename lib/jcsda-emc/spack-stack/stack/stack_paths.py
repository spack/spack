import os

import spack

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


common_path = stack_path('configs', 'common')
site_path = stack_path('configs', 'sites')
container_path = stack_path('configs', 'containers')
template_path = stack_path('configs', 'templates')
