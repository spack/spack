import sys
import itertools


def zip(*args, **kwargs):
    if sys.version_info[0] == 3:
        return itertools.zip(*args, **kwargs)
    return itertools.izip(*args, **kwargs)


def zip_longest(*args, **kwargs):
    if sys.version_info[0] == 3:
        return itertools.zip_longest(*args, **kwargs)
    return itertools.izip_longest(*args, **kwargs)
