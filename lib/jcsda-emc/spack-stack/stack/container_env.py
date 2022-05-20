import os
import spack
import spack.util.spack_yaml as syaml
from spack.extensions.stack.stack_env import StackEnv, stack_path, app_path
import copy

container_path = os.path.join(stack_path(), 'configs', 'containers')


class StackContainer():
    """Represents an abstract container. It takes in a
    container template (spack.yaml), the specs from an app, and
    its packages.yaml versions then writes out a merged file.
    """

    def __init__(self, container, app, name, dir, base_packages) -> None:
        self.app = app
        self.container = container

        test_path = os.path.join(container_path, container + '.yaml')
        if os.path.exists(test_path):
            self.container_path = test_path
        elif os.path.isabs(container):
            self.container_path = container
        else:
            raise Exception("Invalid container {}".format(self.container))

        if os.path.isabs(app):
            self.app_path = app
        elif os.path.exists(os.path.join(app_path, app)):
            self.app_path = os.path.join(app_path, app)
        else:
            raise Exception("Invalid app")

        self.name = name if name else '{}.{}'.format(app, container)

        self.dir = dir
        self.env_dir = os.path.join(self.dir, self.name)
        self.base_packages = base_packages

    def write(self):
        """Merge base packages and app's spack.yaml into
        output container file.
        """
        app_env = os.path.join(self.app_path, 'spack.yaml')
        with open(app_env, 'r') as f:
            # Spack uses :: to override settings.
            # but it's not understood when used in a spack.yaml
            filedata = f.read()
            filedata.replace('::', ':')
            filedata = filedata.replace('::', ':')
            app_yaml = syaml.load_config(filedata)

        with open(self.container_path, 'r') as f:
            container_yaml = syaml.load_config(f)

        # Create copy so we can modify it
        original_yaml = copy.deepcopy(container_yaml)

        with open(self.base_packages, 'r') as f:
            filedata = f.read()
            filedata = filedata.replace('::', ':')
            packages_yaml = syaml.load_config(filedata)

        if 'packages' not in container_yaml['spack']:
            container_yaml['spack']['packages'] = {}

        container_yaml['spack']['packages'] = spack.config.merge_yaml(
            container_yaml['spack']['packages'], packages_yaml['packages'])

        container_yaml = spack.config.merge_yaml(container_yaml, app_yaml)
        # Merge the original back in so it takes precedence
        container_yaml = spack.config.merge_yaml(container_yaml, original_yaml)

        container_yaml['spack']['container']['labels']['app'] = self.app


        os.makedirs(self.env_dir, exist_ok=True)

        with open(os.path.join(self.env_dir, 'spack.yaml'), 'w') as f:
            syaml.dump_config(container_yaml, stream=f)
