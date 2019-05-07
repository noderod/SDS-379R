"""
BASICS

Computes the sha256 checksum of a file
"""


import hashlib



def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()


# Reads a file by block
def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)




# Checks the file checksum using sha256
def csum(filename):
    return hash_bytestr_iter(open(filename, "rb"), hashlib.sha256())




#[(fname, hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha256()))
#    for fname in fnamelst]

print(csum("gromacs-test/#mdout.mdp.4#"))
print(csum("gromacs-test/#mdout.mdp.5#"))
