import hmac
import hashlib
import struct

from django.contrib.auth.backends import ModelBackend

import snotes20.models as models


class NModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        # don't allow any non-migrated users to auth with ModelBackend
        try:
            user = models.NUser.objects.get(username=username)
            if not user.migrated:
                return None
        except models.NUser.DoesNotExist:
            return None

        return super(NModelBackend, self).authenticate(username, password, **kwargs)


class ShowPadBackend(object):

    def authenticate(self, username=None, password=None):
        if username is None or password is None:
            return None

        try:
            user = models.NUser.objects.get(username=username)

            if user.old_password is None or user.migrated:
                return None

            pw = bytearray(password, 'ascii')
            old_pw = user.old_password.split('$')
            salt = bytearray(old_pw[0], 'ascii')
            iterations = int(old_pw[1])

            hash1 = pbkdf2(hashlib.sha1, pw, salt, iterations, 32)
            hash2 = bytearray.fromhex(old_pw[2])

            if hash1 == hash2:
                return user
        except models.NUser.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return models.NUser.objects.get(pk=user_id)
        except models.NUser.DoesNotExist:
            return None


def pbkdf2(digestmod, password: 'bytes', salt, count, dk_length) -> 'bytes':
    '''
    PBKDF2, from PKCS #5 v2.0:
        http://tools.ietf.org/html/rfc2898

    For proper usage, see NIST Special Publication 800-132:
        http://csrc.nist.gov/publications/PubsSPs.html

    The arguments for this function are:

        digestmod
            a crypographic hash constructor, such as hashlib.sha256
            which will be used as an argument to the hmac function.
            Note that the performance difference between sha1 and
            sha256 is not very big. New applications should choose
            sha256 or better.

        password
            The arbitrary-length password (passphrase) (bytes)

        salt
            A bunch of random bytes, generated using a cryptographically
            strong random number generator (such as os.urandom()). NIST
            recommend the salt be _at least_ 128bits (16 bytes) long.

        count
            The iteration count. Set this value as large as you can
            tolerate. NIST recommend that the absolute minimum value
            be 1000. However, it should generally be in the range of
            tens of thousands, or however many cause about a half-second
            delay to the user.

        dk_length
            The lenght of the desired key in bytes. This doesn't need
            to be the same size as the hash functions digest size, but
            it makes sense to use a larger digest hash function if your
            key size is large.

    '''
    def pbkdf2_function(pw, salt, count, i):
        # in the first iteration, the hmac message is the salt
        # concatinated with the block number in the form of \x00\x00\x00\x01
        r = u = hmac.new(pw, salt + struct.pack(">i", i), digestmod).digest()
        for i in range(2, count + 1):
            # in subsequent iterations, the hmac message is the
            # previous hmac digest. The key is always the users password
            # see the hmac specification for notes on padding and stretching
            u = hmac.new(pw, u, digestmod).digest()
            # this is the exclusive or of the two byte-strings
            r = bytes(i ^ j for i, j in zip(r, u))
        return r
    dk, h_length = b'', digestmod().digest_size
    # we generate as many blocks as are required to
    # concatinate to the desired key size:
    blocks = (dk_length // h_length) + (1 if dk_length % h_length else 0)
    for i in range(1, blocks + 1):
        dk += pbkdf2_function(password, salt, count, i)
    # The length of the key wil be dk_length to the nearest
    # hash block size, i.e. larger than or equal to it. We
    # slice it to the desired length befor returning it.
    return dk[:dk_length]


def testHashing():
    raw_password = bytearray("shie9EiSh0", 'ascii')
    salt = bytearray('1957b4c6bbe0fc157a32f36db442addbe46f1d8ce0f68822095dfedddca8519b058d30731f9fe37de96d949c3681d00d6d7eb6e7724c8174770010f26854f0fd855f768666bdedafdd4360882d722f2b39aee5ac7d03491c3050e8db81979caa78090f1c2407d4d1e00228f7191252aa572d7440076c4612f695baa0d4e6d2d8', 'ascii')
    hash1 = bytearray.fromhex("7ecae6459b6178cb67190c0885f3074bcbe3e1a50e470b249eb30df855615f72")
    iterations = 92141

    hash2 = pbkdf2(hashlib.sha1, raw_password, salt, iterations, 32)

    assert hash1 == hash2

testHashing()
