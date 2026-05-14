# File: src/ftwpki/ca_root_creator/programms.py
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

from ftwpki.baselibs.core import (
    save_pem,
)
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.toml_utils import toml2dn
from ftwpki.ca_root_creator.caroot import CertificateAuthority
from ftwpki.ca_root_creator.cli_parser import CaInitParser


def prog_ca_root_creator_cert(argv: list[str] | None = None) -> int:
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
        ca_root_creator = CertificateAuthority(
            common_name=args.commonName,
            country=args.countryName,
            state=args.stateOrProvinceName,
            location=args.localityName,
            organization=args.organizationName,
            organizational_unit=args.organizationalUnitName,
        )
        ca_root_creator.generate_key_pair(
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename=args.passphrasefile,
                password=getpass.getpass("Enter Passphrase:"),
            )
        )
        save_pem(ca_root_creator.private_key, Path(f"{args.privatdir}/{args.private_key}"), is_private=True)
        save_pem(ca_root_creator.public_key, Path(f"{args.public_key}"), is_private=False)
        ca_root_creator.create_root_certificate(
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename=args.passphrasefile,
                password=getpass.getpass("Enter Passphrase:"),
            ),
            days=20 * 370,
        )
        save_pem(ca_root_creator.certificate, Path(f"{args.certificate}"), is_private=False)
        return 0
    except Exception as e:
        print(e)
        return 1



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
    # test_file = testfiles_dir / "get_started_programms.rst"

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
