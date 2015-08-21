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


class Database(object):
    def __init__(self,file_name="specDB.yaml"):
        """
        Create an empty Database
        Location defaults to root/specDB.yaml
        """
        self.file_name = file_name
        self.data = []

    
    def from_yaml(self,stream):
        """
        Fill database from YAML
        Translate the spec portions from node-dict form to spec from
        """
        try:
            file = yaml.load(stream)
        except MarkedYAMLError, e:
            raise SpackYAMLError("error parsing YAML database:", str(e))

        if file==None:
            return

        for sp in file['database']:
            spec = Spec.from_node_dict(sp['spec'])
            path = sp['path']
            db_entry = {'spec': spec, 'path': path}
            self.data.append(db_entry)

                                      
    @staticmethod
    def read_database(root):
        """Create a Database from the data in the standard location"""
        database = Database()
        full_path = join_path(root,database.file_name)
        if os.path.isfile(full_path):
            with open(full_path,'r') as f:
                database.from_yaml(f)
        else:
            with open(full_path,'w+') as f:
                database.from_yaml(f)

        return database

    
    def write_database_to_yaml(self,stream):
        """
        Replace each spec with its dict-node form
        Then stream all data to YAML
        """
        node_list = []
        for sp in self.data:
            node = {}
            node['spec']=Spec.to_node_dict(sp['spec'])
            node['spec'][sp['spec'].name]['hash']=sp['spec'].dag_hash()
            node['path']=sp['path']
            node_list.append(node)
        return yaml.dump({ 'database' : node_list},
                         stream=stream, default_flow_style=False)


    def write(self,root):
        """Write the database to the standard location"""
        full_path = join_path(root,self.file_name)
        #test for file existence
        with open(full_path,'w') as f:
            self.write_database_to_yaml(f)


    @staticmethod
    def add(root, spec, path):
        """Read the database from the standard location
        Add the specified entry as a dict
        Write the database back to memory

        TODO: Caching databases
        """
        database = Database.read_database(root)
        
        spec_and_path = {}
        spec_and_path['spec']=spec
        spec_and_path['path']=path
        
        database.data.append(spec_and_path)
        
        database.write(root)


    @staticmethod
    def remove(root, spec):
        """
        Reads the database from the standard location
        Searches for and removes the specified spec
        Writes the database back to memory

        TODO: Caching databases
        """
        database = Database.read_database(root)

        for sp in database.data:
            #This requires specs w/o dependencies, is that sustainable?
            if sp['spec'] == spec:
                database.data.remove(sp)

        database.write(root)
