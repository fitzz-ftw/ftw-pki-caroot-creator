# File: src/ftwpki/ca_root/cli_parser.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2
"""
cli_parser
===============================

Command-line interface parser for Root-CA initialization, handling
Distinguished Name data and file path configuration. (rw)
"""

from argparse import Namespace
from pathlib import Path
from typing import cast

from ftwpki.baselibs.cli_parser import (
    DistinguishedNameParser,
)
from ftwpki.ca_root.protocols import CaInitProtocol


# CLASS - CaInitParser
class CaInitParser(DistinguishedNameParser):
    """
    Parser for Root-CA initialization arguments. (rw)

    Extends the DistinguishedNameParser to include specific arguments for
    passphrase secrets, key storage, and certificate filenames.
    """

    def _setup_parser(self) -> None:
        """
        Configure the argument parser with Root-CA specific options. (ro)

        Sets up arguments for the passphrase file, private/public keys,
        certificates, and the private storage directory.
        """
        super()._setup_parser()
        self.add_argument(
            "passphrasefile", help="Filename of the encrypted secret containing the CA passphrase."
        )
        self.add_argument(
            "-k",
            "--key",
            "--private-key",
            dest="private_key",
            default="",
            help="Optional specific filename for the generated private key.",
        )
        self.add_argument(
            "-c",
            "--cert",
            "--certificate",
            dest="certificate",
            default="",
            help="Optional specific filename for the root certificate.",
        )
        self.add_argument(
            "-p",
            "--pub",
            "--public-key",
            dest="public_key",
            default="",
            help="Optional specific filename for the public key.",
        )
        self.add_argument(
            "--privatdir",
            dest="privatdir",
            default="",
            help="Directory path for private key storage (overrides default).",
        )

    def parse_args(
        self, args: list[str] | None = None, namespace: Namespace | None = None
    ) -> CaInitProtocol:
        """
        Parse command-line arguments and cast to CaInitProtocol. (ro)

        :param args: List of command-line argument strings.
        :param namespace: Existing Namespace object to populate.
        :returns: Arguments adhering to the CaInitProtocol interface.
        """
        return cast(CaInitProtocol, super().parse_args(args, namespace))


# !CLASS - CaInitParser

# FUNCTION - get_ca_init_parser
def get_ca_init_parser() -> CaInitParser:
    """
    Factory function to create and return a configured CaInitParser instance. (ro)

    :returns: An instance of CaInitParser ready for argument parsing.
    """
    parser = CaInitParser(
        prog="ftwpkicaroot",
        description="Initialize a Root-CA with specified parameters.",
        epilog="Example usage: ftwpkicaroot --help for more information.",
    )
    return parser   
# !FUNCTION - get_parser


if __name__ == "__main__": # pragma: no cover
    from doctest import FAIL_FAST, testfile
    
    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_cli_parser.rst"
    
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
