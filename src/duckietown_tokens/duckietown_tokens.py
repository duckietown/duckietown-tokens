import json
import os

import base58
import ecdsa
from ecdsa import SigningKey, VerifyingKey

from . import logger

__all__ = [
    "DuckietownToken",
    "InvalidToken",
    "verify_token",
    "create_signed_token",
    "get_signing_key",
    "get_id_from_token",
]

private = "key1.pem"
public = "key1-pub.pem"
curve = ecdsa.NIST192p


class DuckietownToken:
    VERSION = "dt1"
    payload: bytes
    signature: bytes

    def __init__(self, payload: bytes, signature: bytes):
        self.payload = payload
        self.signature = signature

    def as_string(self):
        payload_58 = base58.b58encode(self.payload).decode("utf-8")
        signature_58 = base58.b58encode(self.signature).decode("utf-8")
        return "%s-%s-%s" % (DuckietownToken.VERSION, payload_58, signature_58)

    @staticmethod
    def from_string(s: str) -> "DuckietownToken":
        p = s.split("-")
        if len(p) != 3:
            raise ValueError(p)
        if p[0] != DuckietownToken.VERSION:
            raise ValueError(p[0])
        payload_base58 = p[1]
        signature_base58 = p[2]
        payload = base58.b58decode(payload_base58)
        signature = base58.b58decode(signature_base58)
        return DuckietownToken(payload, signature)


def get_signing_key() -> SigningKey:
    """ Loads the key in the location "privatE" """
    if not os.path.exists(private):
        logger.info("Creating private key %r" % private)
        sk0 = SigningKey.generate(curve=curve)
        with open(private, "wb") as f:
            f.write(sk0.to_pem())

        vk = sk0.get_verifying_key()
        with open(public, "wb") as f:
            f.write(vk.to_pem())
    with open(private, "r") as _:
        pem = _.read()
    sk = SigningKey.from_pem(pem)
    return sk


def get_verify_key() -> VerifyingKey:
    key1 = """-----BEGIN PUBLIC KEY-----
MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEQr/8RJmJZT+Bh1YMb1aqc2ao5teE
ixOeCMGTO79Dbvw5dGmHJLYyNPwnKkWayyJS
-----END PUBLIC KEY-----"""
    return VerifyingKey.from_pem(key1)


def create_signed_token(payload: bytes) -> DuckietownToken:
    sk: SigningKey = get_signing_key()

    def entropy(numbytes: int) -> bytes:
        s = b"duckietown is a place of relaxed introspection" * 100
        return s[:numbytes]

    logger.info(f"signing payload {payload!r}")
    signature = sk.sign(payload, entropy=entropy)
    return DuckietownToken(payload, signature)


def verify_token(token: DuckietownToken):
    vk: VerifyingKey = get_verify_key()
    return vk.verify(token.signature, token.payload)


class InvalidToken(Exception):
    pass


def get_id_from_token(s: str) -> int:
    """
        Returns a numeric ID from the token, or raises InvalidToken.

    """
    try:
        token = DuckietownToken.from_string(s)
    except ValueError:
        msg = "Invalid token format %r." % s
        raise InvalidToken(msg)
    try:
        data = json.loads(token.payload)
        uid = data["uid"]
        return uid
    except ValueError:
        raise InvalidToken()
