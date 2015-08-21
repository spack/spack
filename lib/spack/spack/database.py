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
import os
import sys
import inspect
import glob
import imp

import time
import copy

from external import yaml
from external.yaml.error import MarkedYAMLError

import llnl.util.tty as tty
from llnl.util.filesystem import join_path
from llnl.util.lang import *

import spack.error
import spack.spec
from spack.spec import Spec
from spack.error import SpackError
from spack.virtual import ProviderIndex
from spack.util.naming import mod_to_class, validate_module_name


def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, **kwargs)
    return converter


class Database(object):
    def __init__(self,root,file_name="specDB.yaml"):
        """
        Create an empty Database
        Location defaults to root/specDB.yaml
        The individual data are dicts containing
        spec: the top level spec of a package
        path: the path to the install of that package
        dep_hash: a hash of the dependence DAG for that package
        """
        self.root = root
        self.file_name = file_name
        self.file_path = join_path(self.root,self.file_name)
        self.data = []
        self.last_write_time = 0


    def from_yaml(self,stream):
        """
        Fill database from YAML, do not maintain old data
        Translate the spec portions from node-dict form to spec from
        """
        try:
            file = yaml.load(stream)
        except MarkedYAMLError, e:
            raise SpackYAMLError("error parsing YAML database:", str(e))

        if file==None:
            return

        self.data = []
        for sp in file['database']:
            spec = Spec.from_node_dict(sp['spec'])
            path = sp['path']
            dep_hash = sp['hash']
            db_entry = {'spec': spec, 'path': path, 'hash':dep_hash}
            self.data.append(db_entry)


    def read_database(self):
        """Reread Database from the data in the set location"""
        if os.path.isfile(self.file_path):
            with open(self.file_path,'r') as f:
                self.from_yaml(f)
        else:
            #The file doesn't exist, construct empty data.
            self.data = []


    def write_database_to_yaml(self,stream):
        """
        Replace each spec with its dict-node form
        Then stream all data to YAML
        """
        node_list = []
        for sp in self.data:
            node = {}
            node['spec']=Spec.to_node_dict(sp['spec'])
#            node['spec'][sp['spec'].name]['hash']=sp['spec'].dag_hash()
            node['hash']=sp['hash']
            node['path']=sp['path']
            node_list.append(node)
        return yaml.dump({ 'database' : node_list},
                         stream=stream, default_flow_style=False)


    def write(self):
        """Write the database to the standard location"""
        #creates file if necessary
        with open(self.file_path,'w') as f:
            self.last_write_time = int(time.time())
            self.write_database_to_yaml(f)


    def is_dirty(self):
        """
        Returns true iff the database file exists
        and was most recently written to by another spack instance.
        """
        return (os.path.isfile(self.file_path) and (os.path.getmtime(self.file_path) > self.last_write_time))


#    @_autospec
    def add(self, spec, path):
        """Re-read the database from the set location if data is dirty
        Add the specified entry as a dict
        Write the database back to memory
        """
        if self.is_dirty():
            self.read_database()

        sph = {}
        sph['spec']=spec
        sph['path']=path
        sph['hash']=spec.dag_hash()

        self.data.append(sph)

        self.write()


    @_autospec
    def remove(self, spec):
        """
        Re-reads the database from the set location if data is dirty
        Searches for and removes the specified spec
        Writes the database back to memory
        """
        if self.is_dirty():
            self.read_database()

        for sp in self.data:

            if sp['hash'] == spec.dag_hash() and sp['spec'] == Spec.from_node_dict(spec.to_node_dict()):
                self.data.remove(sp)

        self.write()


    @_autospec
    def get_installed(self, spec):
        """
        Get all the installed specs that satisfy the provided spec constraint
        """
        return [s for s in self.installed_package_specs() if s.satisfies(spec)]


    @_autospec
    def installed_extensions_for(self, extendee_spec):
        """
        Return the specs of all packages that extend
        the given spec
        """
        for s in self.installed_package_specs():
            try:
                if s.package.extends(extendee_spec):
                    yield s.package
            except UnknownPackageError, e:
                continue
            #skips unknown packages
            #TODO: conditional way to do this instead of catching exceptions


    def installed_package_specs(self):
        """
        Read installed package names from the database
        and return their specs
        """
        if self.is_dirty():
            self.read_database()

        installed = []
        for sph in self.data:
            sph['spec'].normalize()
            sph['spec'].concretize()
            installed.append(sph['spec'])
        return installed


    def installed_known_package_specs(self):
        """
        Read installed package names from the database.
        Return only the specs for which the package is known
        to this version of spack
        """
        return [s for s in self.installed_package_specs() if spack.db.exists(s.name)]

