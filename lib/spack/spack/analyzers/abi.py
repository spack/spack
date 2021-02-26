# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from .base import AnalyzerBase

class LibabigailAnalyzer(AnalyzerBase):

    name = "libabigail"
    outfile = "spack-analyzer-libabigail.json"
    description = "Application Binary Interface (ABI) features for objects"
        
    def __init__(self, spec): 
        super().__init__(spec)
       
    def run(self):
        """Given a directory name, return the json file to save the result to
        """
        # not written yet
        return {self.name: {}}
