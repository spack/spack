# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# Holds all known formatters

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