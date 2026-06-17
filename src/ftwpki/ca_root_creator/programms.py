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

from ftwpki.baselibs._cli_parser import PKIBaseParser
from ftwpki.baselibs.core import (
    RSAPrivateKey,
    load_certificate_from_pem,
    load_private_key_from_pem,
    x509,
)
from ftwpki.baselibs.package import PKIPackage
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.toml_utils import toml2dn
from ftwpki.ca_root_creator.caroot import CertificateAuthority
from ftwpki.ca_root_creator.cli_parser import CaInit, CaInitArguments, ca_init_parser


def prog_ca_root_creator_cert(argv: list[str] | None = None) -> int:
    """
    Entry point for initializing a new Root-CA. (rw)

    Processes CLI arguments, generates the RSA key pair, and creates the
    self-signed root certificate.

    :param argv: Optional list of command-line arguments.
    :returns: Exit code (0 for success, 1 for error).
    """
    try:
        # SECTION - Configuration
        pki_file: Path|None = None
        pre_parser: PKIBaseParser[CaInit]  = ca_init_parser(add_help=False, allow_abbrev=False)
        pre_args, _ = pre_parser.parse_known_args(argv)
        ca_parser: PKIBaseParser[CaInit] = ca_init_parser()
        ca_parser.set_defaults(
            **toml2dn(Path(pre_args.conf_file).read_text())
        ) if pre_args.conf_file else ...
        del pre_parser
        args: CaInitArguments = ca_parser.parse_args(argv)
        conf_file:Path = Path(args.conf_file)
        pass_file: Path = Path(args.passphrasefile)
        # !SECTION - Configuration
        # SECTION - Passwordhandling
        pwd_man: PasswordManager = PasswordManager(private_dir="")
        password: str  = getpass.getpass("Enter Passphrase:")
        # !SECTION - Passwordhandling
        # SECTION - Certificatecreating
        ca_root_creator: CertificateAuthority = CertificateAuthority(
            common_name=args.commonName,
            country=args.countryName,
            state=args.stateOrProvinceName,
            location=args.localityName,
            organization=args.organizationName,
            organizational_unit=args.organizationalUnitName,
        )
        ca_root_creator.create_root_certificate(
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename=args.passphrasefile,
                password=password,
            ),
            days=20 * 370,
        )
        
        private_key: RSAPrivateKey=load_private_key_from_pem(pem_data=ca_root_creator.private_key, 
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename= args.passphrasefile,
                password = password))
        
        del password
        cert_obj: x509.Certificate = load_certificate_from_pem(ca_root_creator.certificate)
        # SECTION - Certificatecreating

        #SECTION - Pack PKI-Container
        pki_pack: PKIPackage = PKIPackage()
        pki_pack.additional_files["ca_root.policy"]=conf_file.read_bytes()
        pki_pack.additional_files[pass_file.name]=pass_file.read_bytes()
        pki_pack.message = pass_file.name
        pki_pack.additional_files["CA.key.pem"]=ca_root_creator.private_key
        pki_pack.recipient_cert=cert_obj
        pki_pack.caroot_cert=cert_obj
        pki_pack.private_key=private_key
        pki_pack.ca_cert=cert_obj
        pki_file = pki_pack.save(conf_file)
        # SECTION - Pack PKI-Container
        # SECTION - Cleanup CWD   
        pass_file.unlink()
        conf_file.unlink()
        # !SECTION - Cleanup CWD
        return 0
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        print(e)
        pki_file.unlink() if pki_file and pki_file.exists() else ...
        return 1


if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    # be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        "get_started_programms.rst",
        "get_started_run_programms.rst",
        "get_started_cli_parser.rst",
        "get_started_caroot.rst",
        "get_started_protocols.rst",
                  ]

    for file in test_files:
        test_file = testfiles_dir / file
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
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(
                    f"\nKeep going! You already passed {passed_files} files "
                    f"with {test_sum} tests before this hit."
                )
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")
