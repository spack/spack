# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# Holds all known formatters
"""Generators that support writing out pipelines for various CI platforms,
using a common pipeline graph definition.
"""
import spack.error

#: Registered pipeline generation methods
_generators = {}


def generator(name):
    """Decorator to register a pipeline generator method.

    A generator method should take PipelineDag, SpackCIConfig, and
    PipelineOptions arguments, and should produce a pipeline file.

    Args:
        name: pipeline target name
    """

    def _decorator(generate_method):
        _generators[name] = generate_method
        return generate_method

    return _decorator


def get_generator(name):
    """Retrieve the registered pipeline generator method.

    Args:
        name: pipeline target name

    Returns: The pipeline's generator method

    Raises:
        UnknownGeneratorException: no generator method for that target
    """
    try:
        return _generators[name]
    except KeyError:
        raise UnknownGeneratorException(name)


class UnknownGeneratorException(spack.error.SpackError):
    def __init__(self, generator_name):
        super().__init__(f"No registered pipeline generator for {generator_name}")
