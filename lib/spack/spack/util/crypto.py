import hashlib
from contextlib import closing

"""Set of acceptable hashes that Spack will use."""
_acceptable_hashes = [
    hashlib.md5,
    hashlib.sha1,
    hashlib.sha224,
    hashlib.sha256,
    hashlib.sha384,
    hashlib.sha512 ]

"""Index for looking up hasher for a digest."""
_size_to_hash = { h().digest_size : h for h in _acceptable_hashes }


def checksum(hashlib_algo, filename, **kwargs):
    """Returns a hex digest of the filename generated using an
       algorithm from hashlib.
    """
    block_size = kwargs.get('block_size', 2**20)
    hasher = hashlib_algo()
    with closing(open(filename)) as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()



class Checker(object):
    """A checker checks files against one particular hex digest.
       It will automatically determine what hashing algorithm
       to used based on the length of the digest it's initialized
       with.  e.g., if the digest is 32 hex characters long this will
       use md5.

       Example: know your tarball should hash to 'abc123'.  You want
       to check files against this.  You would use this class like so::

          hexdigest = 'abc123'
          checker = Checker(hexdigest)
          success = checker.check('downloaded.tar.gz')

       After the call to check, the actual checksum is available in
       checker.sum, in case it's needed for error output.

       You can trade read performance and memory usage by
       adjusting the block_size optional arg.  By default it's
       a 1MB (2**20 bytes) buffer.
    """
    def __init__(self, hexdigest, **kwargs):
        self.block_size = kwargs.get('block_size', 2**20)
        self.hexdigest = hexdigest
        self.sum       = None

        bytes = len(hexdigest) / 2
        if not bytes in _size_to_hash:
            raise ValueError(
                'Spack knows no hash algorithm for this digest: %s' % hexdigest)

        self.hash_fun = _size_to_hash[bytes]


    @property
    def hash_name(self):
        """Get the name of the hash function this Checker is using."""
        return self.hash_fun().name


    def check(self, filename):
        """Read the file with the specified name and check its checksum
           against self.hexdigest.  Return True if they match, False
           otherwise.  Actual checksum is stored in self.sum.
        """
        self.sum = checksum(
            self.hash_fun, filename, block_size=self.block_size)
        return self.sum == self.hexdigest

