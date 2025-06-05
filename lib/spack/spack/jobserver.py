# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module encapsulates make jobserver functionality.

If a jobserver is enabled, make jobs will be dyamically allocated
to package builds during the installation process. 
"""

import enum

class JobserverType(enum.Enum):
    """Possible jobserver states"""
    
    # Do not set up jobserver. 
    NONE = enum.auto()

    # Set up FIFO implementation of jobserver.
    FIFO = enum.auto()

    # Set up fd implementation of jobserver.
    FD = enum.auto()


# make the calls to the packages to see what type of make they use (if they do)
    # return the max value assinment

if js_type == JobserverType.NONE:
    pass

if js_type == Jo
    
