##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import spack
import spack.config
import llnl.util.tty as tty

class PackageConfig(object):
    """A class for parsing the package information in the .spackconfig file"""
    packages = []
    fields = [ 'symlinks', 'prefix', 'srcdir', 'version_order', 'compiler_order', 'compilerver_order', 'variant_order', 'architecture_order' ]

    def __init__(self):
        config = spack.config.get_config()
        for package in config.get_section_names('package'):
            field_list = []
            for field in self.fields:
                if config.has_value('package', package, field):
                    field_list.append((field, config.get_value('package', package, field)))
            self.packages.append((package, field_list))

    
    def multifield_for_pkgname(self, pkgname, field):
        result = []
        for (package, config_field_values) in self.packages:
            if package != 'default' and pkgname != package:
                continue
            for (config_field, config_value) in config_field_values:
                if config_field != field:
                    continue
                value_list = config_value.split(':')
                for values in value_list:
                    result.extend(values.split(','))
        return result


    multifield_cache = {}
    def lookup_multifield_for_pkgname(self, pkgname, field):
        if not (pkgname, field) in self.multifield_cache:
            self.multifield_cache[(pkgname, field)] = self.multifield_for_pkgname(pkgname, field)
        return self.multifield_cache[(pkgname, field)]

        
    def singlefield_for_pkgname(self, pkgname, field):
        result = None
        result_package = None
        default_value = None

        for (package, config_field_values) in self.packages:
            if package != 'default' and pkgname != package:
                continue
            for (config_field, config_value) in config_field_value:
                if config_field != field:
                    continue
                if result and result != config_value:
                    tty.die("In spackconfig packages, %s settings from %s and %s conflict for pkgname %s" %
                            field, package, result_package, string(pkgname))
                if package != 'default':
                    result = config_value
                    result_package = package
                else:
                    default_value = config_value
        if not result and default_value:
            result = default_value
        return result


    singlefield_cache = {}
    def lookup_singlefield_for_pkgname(self, pkgname, field):
        if not (pkgname, field) in self.singlefield_cache:
            self.singlefield_cache[(pkgname, field)] = self.singlefield_for_pkgname(pkgname, field)
        return self.singlefield_cache[(pkgname, field)]

        
    def symlinks_for_pkgname(self, pkgname):
        return self.lookup_multifield_for_pkgname(pkgname, 'symlinks')
    

    def prefix_for_pkgname(self, pkgname):
        return self.lookup_singlefield_for_pkgname(pkgname, 'prefix')

        
    def srcdir_for_pkgname(self, pkgname):
        return self.lookup_singlefield_for_pkgname(pkgname, 'srcdir')
        
            
    def compiler_order_for_pkgname(self, pkgname):
        return self.lookup_singlefield_for_pkgname(pkgname, 'compiler_order')

    
    def version_order_for_pkgname(self, pkgname):
        return self.lookup_singlefield_for_pkgname(pkgname, 'version_order')

    def compilerver_order_for_pkgname(self, pkgname):
        return self.lookup_singlefield_for_pkgname(pkgname, 'compilerver_order')

    def component_compare(self, pkgname, component, a, b, reverse_natural_compare=False):
        list = self.lookup_multifield_for_pkgname(pkgname, component + '_order')
        a_in_list = str(a) in list
        b_in_list = str(b) in list
        if a_in_list and not b_in_list:
            return -1
        elif b_in_list and not a_in_list:
            return 1

        cmp_a = None
        cmp_b = None
        if not a_in_list and not b_in_list:
            cmp_a = a
            cmp_b = b
        else:
            cmp_a = list.index(str(a))
            cmp_b = list.index(str(b))
        
        reverse = -1 if reverse_natural_compare else 1
        if cmp_a < cmp_b:
            return -1 * reverse
        elif cmp_a > cmp_b:
            return 1 * reverse
        else:
            return 0

    def component_list_compare(self, pkgname, component, list_a, list_b):
        list = self.lookup_multifield_for_pkgname(pkgname, component + '_order')
        for i in list:
            a_in_list = False
            b_in_list = False
            for a in list_a:
                if i == str(a):
                    a_in_list = True
                    break
            for b in list_b:
                if i == str(b):
                    b_in_list = True
                    break            
            if a_in_list and not b_in_list:
                return -1
            elif b_in_list and not a_in_list:
                return 1
        return list_a.__cmp__(list_b)
