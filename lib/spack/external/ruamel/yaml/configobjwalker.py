# coding: utf-8

import warnings
from ruamel.yaml.util import configobj_walker as new_configobj_walker


def configobj_walker(cfg):
    warnings.warn("configobj_walker has move to ruamel.yaml.util, please update your code")
    return new_configobj_walker(cfg)
