# File: src/ftwpki/ca_root/cli_parser.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2
"""
cli_parser
===============================


Modul cli_parser documentation
"""

from argparse import Namespace
from pathlib import Path
from typing import cast

from ftwpki.baselibs.cli_parser import (
    DistinguishedNameParser,
)
from ftwpki.ca_root.protocols import CaInitProtocol


class CaInitParser(DistinguishedNameParser):
    def _setup_parser(self: "CaInitParser") -> None:
        super()._setup_parser() 
        self.add_argument("passphrasefile")
        self.add_argument("-k", "--key", 
                          "--private-key", 
                          dest="private_key",
                          default="",
                          )
        self.add_argument("-c", "--cert", "--certificate", 
                          dest="certificate",
                          default="",
                          )
        self.add_argument(
                            "-p",
                            "--pub",
                            "--public-key",
                            dest="public_key",
                            default="",
                        )
        self.add_argument("--privatdir", 
                          dest="privatdir",
                          default="")

    def parse_args(
        self, args: list[str] | None = None, namespace: Namespace | None = None
    ) -> CaInitProtocol:
        return cast(CaInitProtocol,super().parse_args(args, namespace))    
        




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
