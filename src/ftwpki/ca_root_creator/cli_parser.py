# File: src/ftwpki/ca_root_creator/cli_parser.py
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
    _HELP,
    DistinguishedNameParser,
    load_help_entries,
)
from ftwpki.ca_root_creator.protocols import CaInitProtocol

HELP_FILE = Path(__file__).parent.joinpath("cli_parser.help")


load_help_entries(_HELP, HELP_FILE)

# print(MY)


LANG="en"

# CLASS - CaInitParser
class CaInitParser(DistinguishedNameParser):
    """
    Parser for Root-CA initialization arguments. (rw)

    Extends the DistinguishedNameParser to include specific arguments for
    passphrase secrets, key storage, and certificate filenames.
    """
    def __init__(self, *args, run_setup=True, **kwargs) -> None:
        """
        Initialize the CaInitParser instance. (ro)

        Calls the base class constructor and sets up the argument 
        parser with Root-CA specific options.
        """
        super().__init__(*args, run_setup=False, **kwargs)
        self._help.update("rootca")
        if run_setup:
            self._setup_parser()


    def _setup_parser(self) -> None:
        """
        Configure the argument parser with Root-CA specific options. (ro)

        Sets up arguments for the passphrase file, private/public keys,
        certificates, and the private storage directory.
        """
        super()._setup_parser()
        self.add_argument(
            "passphrasefile",
            nargs="?" if self._preparser else None,
            help=self._help(
                "passphrasefile"
            ),  # "Filename of the encrypted secret containing the CA passphrase.",
        )
        self.add_argument(
            "conf_file",
            help=self._help("conf_file"),  # "Path to the TOML configuration file.",
            nargs="?" if self._preparser else None,
            metavar="configfile",
        )
        self.add_argument(
            "-k",
            "--key",
            "--key-name",
            dest="key_name",
            default="",
            help=self._help(
                "key_name"
            ),  # "Optional specific filename for the generated private key.",
        )
        self.add_argument(
            "-c",
            "--cert",
            "--certificate",
            dest="certificate",
            default="",
            help=self._help(
                "certificate"
            ),  # "Optional specific filename for the root certificate.",
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
        args_parsed = cast(Namespace, super().parse_args(args, namespace))
        base_name = args_parsed.key_name
        args_parsed.private_key = f"{base_name}.key.pem" if base_name else ""
        args_parsed.public_key = f"{base_name}.pub.pem" if base_name else ""
        return cast(CaInitProtocol, args_parsed)


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
    passed_files = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"

    test_files = [
        "test_new_parser.rst",
        #   "get_started_cli_parser.rst",
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
