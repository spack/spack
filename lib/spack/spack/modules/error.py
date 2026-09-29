# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Errors and exceptions for the modules package."""

import spack.error


class ModulesError(spack.error.SpackError):
    """Base error for modules."""


class ModuleNotFoundError(ModulesError):
    """Raised when a module cannot be found for a spec"""


class DefaultTemplateNotDefined(AttributeError, ModulesError):
    """Raised if ``default_template`` has not been specified in the derived class."""


class HideCmdFormatNotDefined(AttributeError, ModulesError):
    """Raised if ``hide_cmd_format`` has not been specified in the derived class."""


class ModulercHeaderNotDefined(AttributeError, ModulesError):
    """Raised if ``modulerc_header`` has not been specified in the derived class."""


class ModulesTemplateNotFoundError(ModulesError, RuntimeError):
    """Raised if the template for a module file was not found."""


class CoreCompilersNotFoundError(spack.error.SpackError, KeyError):
    """Raised if ``core_compilers`` has not been specified in the configuration file."""
