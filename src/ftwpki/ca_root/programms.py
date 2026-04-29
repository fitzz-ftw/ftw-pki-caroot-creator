# File: src/ftwpki/ca_root/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================

Main entry points for Root-CA initialization and certificate signing. (rw)
"""

import getpass
from pathlib import Path

from ftwpki.baselibs.cli_parser import CSRSigningParser
from ftwpki.baselibs.core import (
    cert_to_record,
    get_subject_dict,
    load_certificate_from_pem,
    load_csr_from_pem,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.openssl_comp import DbOpensslFile
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.policies import IntermediatePolicy
from ftwpki.baselibs.signer import CertificateSigner
from ftwpki.baselibs.toml_utils import toml2dn, toml2dn_policy
from ftwpki.baselibs.transport import encrypt_transport_package
from ftwpki.baselibs.validate import ValidatorDN, validate_and_clamp_validity
from ftwpki.ca_root.caroot import CertificateAuthority
from ftwpki.ca_root.cli_parser import CaInitParser


def prog_ca_root_cert(argv: list[str] | None = None) -> int:
    """
    Entry point for initializing a new Root-CA. (rw)

    Processes CLI arguments, generates the RSA key pair, and creates the
    self-signed root certificate.

    :param argv: Optional list of command-line arguments.
    :returns: Exit code (0 for success, 1 for error).
    """
    try:
        ca_parser = CaInitParser()
        ca_parser.set_defaults(**toml2dn(argv))
        args = ca_parser.parse_args(argv)
        pwd_man = PasswordManager(private_dir=args.privatdir)
        ca_root = CertificateAuthority(
            common_name=args.commonName,
            country=args.countryName,
            state=args.stateOrProvinceName,
            location=args.localityName,
            organization=args.organizationName,
            organizational_unit=args.organizationalUnitName,
        )
        ca_root.generate_key_pair(
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename=args.passphrasefile,
                password=getpass.getpass("Enter Passphrase:"),
            )
        )
        save_pem(ca_root.private_key, Path(f"{args.privatdir}/{args.private_key}"), is_private=True)
        save_pem(ca_root.public_key, Path(f"{args.public_key}"), is_private=False)
        ca_root.create_root_certificate(
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename=args.passphrasefile,
                password=getpass.getpass("Enter Passphrase:"),
            ),
            days=20 * 370,
        )
        save_pem(ca_root.certificate, Path(f"{args.certificate}"), is_private=False)
        return 0
    except Exception as e:
        print(e)
        return 1


# SECTION - Programm Signing
def prog_ca_root_singing(argv: list[str] | None = None) -> int:
    """
    Entry point for signing Certificate Signing Requests (CSRs). (rw)

    Validates the CSR against the CA policy, signs it using the Root-CA key,
    and prepares the transport package.

    :param argv: Optional list of command-line arguments.
    :returns: Exit code (0 for success, 1 for validation error, 2 for other errors).
    """
    try:
        # SECTION - Configuration
        ca_parser = CSRSigningParser()
        ca_parser.set_defaults(**toml2dn_policy(argv))
        args = ca_parser.parse_args(argv)
        # !SECTION - Configuration

        # SECTION - Validating
        ca_cert = load_certificate_from_pem(pem_data=Path(args.certificate).read_bytes())
        csr = load_csr_from_pem(Path(args.certificat_sign_request).read_bytes())
        val_dn = ValidatorDN(args.policy, get_subject_dict(ca_cert))
        validate_result = val_dn.validate(get_subject_dict(csr))
        if not validate_result.is_valid:
            for error in validate_result.errors:
                print(error)
            return 1
        # !SECTION - Validating

        # SECTION - Passwordhandling
        pwd_man = PasswordManager(private_dir=args.private_dir)
        pass_phrase = pwd_man.decrypt_password_file(
            args.passphrasefile, password=getpass.getpass("Enter Password:")
        )
        # !SECTION - Passwordhandling

        # SECTION - Signing
        private_key_obj = load_private_key_from_pem(
            pem_data=Path(args.private_key).read_bytes(), passphrase=pass_phrase
        )
        cert_signer = CertificateSigner(ca_cert=ca_cert, ca_key=private_key_obj)
        policy = IntermediatePolicy(pathlength=args.path_length)
        validity_days = validate_and_clamp_validity(ca_cert, args.validity_days)
        signed_cert = cert_signer.sign(
            csr=csr, policy=policy, validity_days=validity_days.actual_days
        )
        signed_pem = cert_signer.get_pem(signed_cert)
        save_pem(
            data=signed_pem,
            target_path=Path(args.certificat_sign_request).with_suffix(".crt"),
            is_private=True,
        )
        # !SECTION - Signing

        # SECTION - Transferfile
        zipped_data = encrypt_transport_package(
            signed_cert,  # user_cert
            ca_cert,  # root_ca_cert
            private_key_obj,
            signed_cert,  # recipient_cert
            signed_cert,
            ca_cert,
        )

        transfer_file_path = Path(args.certificat_sign_request).with_suffix(".zip.enc")
        transfer_file_path.write_bytes(zipped_data)
        # !SECTION - Transferfile

        # SECTION - Database openssl compatible
        db_dir = Path("db")
        if not db_dir.is_dir():
            db_dir.mkdir(parents=True)
        db_file = DbOpensslFile(db_dir / "index.txt")
        db_file.add_record(
            record=cert_to_record(cert=load_certificate_from_pem(signed_pem), status="V")
        )
        # !SECTION - Database openssl compatible
        return 0
    except Exception as e:
        print(e)
        return 2


# !SECTION - Programm Signing

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
    test_file = testfiles_dir / "get_started_programms.rst"
    test_file = testfiles_dir / "get_started_prog_ca_sign.rst"

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
