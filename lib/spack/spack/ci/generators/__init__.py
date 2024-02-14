# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# Holds all known formatters
"""Generators that support writing out pipelines for various CI platforms,
using a common pipeline graph definition.
"""
import spack.error

_generators = {}


def generator(name):
    """Decorator to register a pipeline generator method.

    Each method should take PipelineDag, SpackCI, PipelineOptions,
    and PruningResults arguments and generate a pipeline file.
    """

    def _decorator(generate_method):
        _generators[name] = generate_method
        return generate_method

    return _decorator


def get_generator(name):
    try:
        return _generators[name]
    except KeyError:
        raise UnknownGeneratorException(name)


class UnknownGeneratorException(spack.error.SpackError):
    def __init__(self, generator_name):
        super().__init__(f"No registered generator for {generator_name}")


# Import specific generators after all the function definitions so that
# each one has access to the registration function, and registration of
# generators will happen automatically.
import spack.ci.generators.gitlab  # noqa: E402
