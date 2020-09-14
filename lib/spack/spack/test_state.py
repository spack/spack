from types import ModuleType

import pickle
import pydoc


patches = None


def append_patch(patch):
    global patches
    if not patches:
        patches = list()
    patches.append(patch)


class TransmitPatches(object):
    def __init__(self, module_patches, class_patches):
        for class_fqn, name, val in class_patches:
            if 'spack.pkg' in class_fqn:
                import pdb; pdb.set_trace()
        self.module_patches = module_patches
        self.class_patches = class_patches

    def apply(self):
        for module_name, attr_name, value in self.module_patches:
            module = __import__(module_name)
            setattr(module, attr_name, value)
        for class_fqn, attr_name, value in self.class_patches:
            cls = pydoc.locate(class_fqn)
            setattr(cls, attr_name, value)


def store_patches():
    global patches
    module_patches = list()
    class_patches = list()
    for patch in patches:
        for target, name, _ in patch._setattr:
            if isinstance(target, ModuleType):
                new_val = getattr(target, name)
                module_name = target.__name__
                module_patches.append((module_name, name, new_val))
            elif isinstance(target, type):
                new_val = getattr(target, name)
                class_fqn = '.'.join([target.__module__, target.__name__])
                class_patches.append((class_fqn, name, new_val))

    return TransmitPatches(module_patches, class_patches)


def clear_patches():
    global patches
    patches = None
