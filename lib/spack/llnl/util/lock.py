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
import fcntl
import errno
import time
import socket


class Read_Lock_Instance(object):
    """
    A context manager for getting shared access to the object lock
    Arguments are lock and timeout (default 5 minutes)
    """
    def __init__(self,lock,timeout = 300):
        self._lock = lock
        self._timeout = timeout
    def __enter__(self):
        self._lock.acquire_read(self._timeout)
    def __exit__(self,type,value,traceback):
        self._lock.release_read()


class Write_Lock_Instance(object):
    """
    A context manager for getting exclusive access to the object lock
    Arguments are lock and timeout (default 5 minutes)
    """
    def __init__(self,lock,timeout = 300):
        self._lock = lock
        self._timeout = timeout
    def __enter__(self):
        self._lock.acquire_write(self._timeout)
    def __exit__(self,type,value,traceback):
        self._lock.release_write()


class Lock(object):
    def __init__(self,file_path):
        self._file_path = file_path
        self._fd = os.open(file_path,os.O_RDWR)
        self._reads = 0
        self._writes = 0


    def acquire_read(self,timeout):
        """
        Implements recursive lock. If held in both read and write mode,
        the write lock will be maintained until all locks are released
        """
        if self._reads == 0 and self._writes == 0:
            self._lock(fcntl.LOCK_SH,timeout)
        self._reads += 1


    def acquire_write(self,timeout):
        """
        Implements recursive lock
        """
        if self._writes == 0:
            self._lock(fcntl.LOCK_EX,timeout)
        self._writes += 1


    def _lock(self,op,timeout):
        """
        The timeout is implemented using nonblocking flock()
        to avoid using signals for timing
        Write locks store pid and host information to the lock file
        Read locks do not store data
        """
        total_time = 0
        while total_time < timeout:
            try:
                fcntl.flock(self._fd, op | fcntl.LOCK_NB)
                if op == fcntl.LOCK_EX:
                    with open(self._file_path,'w') as f:
                        f.write("pid = "+str(os.getpid())+", host = "+socket.getfqdn())
                return
            except IOError as error:
                if error.errno == errno.EAGAIN or error.errno == EACCES:
                    pass
                else:
                    raise
            time.sleep(0.1)
            total_time += 0.1


    def release_read(self):
        """
        Assert there is a lock of the right type to release, recursive lock
        """
        assert self._reads > 0
        if self._reads == 1 and self._writes == 0:
            self._unlock()
        self._reads -= 1


    def release_write(self):
        """
        Assert there is a lock of the right type to release, recursive lock
        """
        assert self._writes > 0
        if self._writes == 1 and self._reads == 0:
            self._unlock()
        self._writes -= 1


    def _unlock(self):
        """
        Releases the lock regardless of mode. Note that read locks may be
        masquerading as write locks at times, but this removes either.
        """
        fcntl.flock(self._fd,fcntl.LOCK_UN)
