##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse
import os.path

import spack.cmd.module as module
import spack.modules as modules
import spack.test.mock_database


class TestModule(spack.test.mock_database.MockDatabase):

    def _get_module_files(self, args):
        return [modules.module_types[args.module_type](spec).file_name
                for spec in args.specs()]

    def test_module_common_operations(self):
        parser = argparse.ArgumentParser()
        module.setup_parser(parser)

        # Try to remove a non existing module [tcl]
        args = parser.parse_args(['rm', 'doesnotexist'])
        self.assertRaises(SystemExit, module.module, parser, args)

        # Remove existing modules [tcl]
        args = parser.parse_args(['rm', '-y', 'mpileaks'])
        module_files = self._get_module_files(args)
        for item in module_files:
            self.assertTrue(os.path.exists(item))
        module.module(parser, args)
        for item in module_files:
            self.assertFalse(os.path.exists(item))

        # Add them back [tcl]
        args = parser.parse_args(['refresh', '-y', 'mpileaks'])
        module.module(parser, args)
        for item in module_files:
            self.assertTrue(os.path.exists(item))

        # TODO : test the --delete-tree option
        # TODO : this requires having a separate directory for test modules

        # Try to find a module with multiple matches
        args = parser.parse_args(['find', 'mpileaks'])
        self.assertRaises(SystemExit, module.module, parser, args)

        # Try to find a module with no matches
        args = parser.parse_args(['find', 'doesnotexist'])
        self.assertRaises(SystemExit, module.module, parser, args)

        # Try to find a module
        args = parser.parse_args(['find', 'libelf'])
        module.module(parser, args)

        # Remove existing modules [dotkit]
        args = parser.parse_args(['rm', '-y', '-m', 'dotkit', 'mpileaks'])
        module_files = self._get_module_files(args)
        for item in module_files:
            self.assertTrue(os.path.exists(item))
        module.module(parser, args)
        for item in module_files:
            self.assertFalse(os.path.exists(item))

        # Add them back [dotkit]
        args = parser.parse_args(['refresh', '-y', '-m', 'dotkit', 'mpileaks'])
        module.module(parser, args)
        for item in module_files:
            self.assertTrue(os.path.exists(item))
        # TODO : add tests for loads and find to check the prompt format
