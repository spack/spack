import hashlib
from contextlib import closing

def md5(filename, block_size=2**20):
    """Computes the md5 hash of a file."""
    md5 = hashlib.md5()
    with closing(open(filename)) as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
