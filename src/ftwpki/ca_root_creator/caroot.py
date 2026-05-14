# File: src/ftwpki/baselibs/caroot.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: GPLv2
"""
caroot
===============================

Core logic for Root Certificate Authority management, including RSA key pair
generation and self-signed X.509 certificate creation. (rw)
"""

import datetime
from pathlib import Path
from typing import cast

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.types import (
    CertificateIssuerPrivateKeyTypes,
    CertificatePublicKeyTypes,
    PrivateKeyTypes,
)

from ftwpki.baselibs.core import create_distinguished_name, generate_rsa_key_pair


# CLASS - CertificateAuthority
class CertificateAuthority:
    """
    Handler for the creation of Root CAs and certificate management. (rw)

    This class manages the CA's identity (Subject), private key generation,
    and the issuance of the self-signed root certificate.
    """

    def __init__(
        self,
        common_name: str,
        country: str,
        state: str,
        location: str,
        organization: str,
        organizational_unit: str = ".",
    ) -> None:
        """
        Initialize CA metadata based on Distinguished Name components. (rw)

        A dot ('.') in organizational_unit prevents the field from being created
        in the final X.509 subject.

        :param common_name: The primary name of the CA (e.g., 'Root CA').
        :param country: Two-letter ISO country code.
        :param state: State or province name.
        :param location: Locality or city name.
        :param organization: Legal name of the organization.
        :param organizational_unit: Department or unit name (use '.' to omit).
        """
        self._subject = create_distinguished_name(
            common_name=common_name,
            country=country,
            state=state,
            location=location,
            organization=organization,
            organizational_unit=organizational_unit,
        )
        self._private_key: bytes = b""
        self._ca_cert: bytes = b""
        self._public_key: bytes = b""

    @property
    def private_key(self) -> bytes:
        """
        The PEM encoded private key of the Root CA. (ro)

        **Security Note:** This data is highly sensitive and must be
        stored securely.

        :returns: The private key as PEM encoded bytes.
        """
        return self._private_key

    @property
    def public_key(self) -> bytes:
        """
        The PEM encoded public key of the Root CA. (ro)

        Extracted as SubjectPublicKeyInfo for verification purposes.

        :returns: The public key as PEM encoded bytes.
        """
        return self._public_key

    @property
    def certificate(self) -> bytes:
        """
        The self-signed Root CA certificate. (ro)

        This certificate serves as the trust anchor for the PKI.

        :returns: The X.509 certificate as PEM encoded bytes.
        """
        return self._ca_cert

    def generate_key_pair(self, passphrase: str) -> None:
        """
        Generate a 4096-bit RSA key pair protected by a passphrase. (rw)

        Uses AES-256-CBC encryption and PBKDF2-HMAC-SHA256 derivation
        for the resulting PEM structure.

        :param passphrase: The strong passphrase for private key encryption.
        :raises ValueError: If the passphrase is empty or '.'.
        """
        if not passphrase or passphrase == ".":
            raise ValueError("Root CA private key MUST be protected by a strong passphrase.")

        private_pem, public_pem = generate_rsa_key_pair(passphrase)

        self._private_key = private_pem
        self._public_key = public_pem

    def create_root_certificate(self, passphrase: str, days: int = 7300) -> None:
        """
        Create a self-signed Root CA certificate with v3 extensions. (rw)

        Automatically generates a key pair if none exists. Sets BasicConstraints
        (CA:True) and KeyUsage (keyCertSign, cRLSign) as critical.

        :param passphrase: Password required to load the internal private key.
        :param days: Validity period in days (default: 7300 / 20 years).
        """
        if not self._private_key:
            self.generate_key_pair(passphrase=passphrase)

        private_key: PrivateKeyTypes = serialization.load_pem_private_key(
            self._private_key, password=passphrase.encode()
        )
        public_key = cast(CertificatePublicKeyTypes, private_key.public_key())

        builder = x509.CertificateBuilder()
        builder = builder.subject_name(self._subject)
        builder = builder.issuer_name(self._subject)
        builder = builder.public_key(public_key)
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        builder = builder.not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=days)
        )

        builder = builder.add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True
        )
        builder = builder.add_extension(
            x509.KeyUsage(
                digital_signature=False,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        builder = builder.add_extension(
            x509.SubjectKeyIdentifier.from_public_key(public_key), critical=False
        )

        issuer_key = cast(CertificateIssuerPrivateKeyTypes, private_key)

        certificate = builder.sign(
            private_key=issuer_key,
            algorithm=hashes.SHA512(),
        )

        self._ca_cert = certificate.public_bytes(serialization.Encoding.PEM)

    def __repr__(self) -> str:
        """
        Return the canonical string representation. (rw)

        :returns: String containing the class name and the subject DN.
        """
        return f"{self.__class__.__name__}(subject={self._subject!r})"


# !CLASS - CertificateAuthority


if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_caroot.rst"

    if test_file.exists():
        print(f"--- Running Doctest for {test_file.name} ---")
        doctestresult = testfile(
            str(test_file),
            module_relative=False,
            verbose=be_verbose,
            optionflags=option_flags,
        )
        test_failed += doctestresult.failed
        test_sum += doctestresult.attempted
        if test_failed == 0:
            print(f"\nDocTests passed without errors, {test_sum} tests.")
        else:
            print(f"\nDocTests failed: {test_failed} tests.")
    else:
        print(f"⚠️ Warning: Test file {test_file.name} not found.")
