# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# Holds all known formatters
"""Formatters that support writing out pipelines for various CI platforms,
using a common pipeline graph definition.
"""
import spack.error

_formatters = {}


def formatter(name):
    """Decorator to register a pipeline formatter method.

    Each method should take PipelineDag, SpackCI, and PipelineOptions
    arguments and generate a pipeline file.
    """

    def _decorator(fmt_method):
        _formatters[name] = fmt_method
        return fmt_method

    return _decorator


def get_formatter(name):
    try:
        return _formatters[name]
    except KeyError:
        raise UnknownFormatterException(name)


class UnknownFormatterException(spack.error.SpackError):
    def __init__(self, formatter_name):
        super().__init__(f"No registered formatter for {formatter_name}")


# Import specific formatters after all the function definitions so that
# each one has access to the registration function, and registration of
# formatters will happen automatically.
import spack.ci.formatters.gitlab  # noqa: E402
