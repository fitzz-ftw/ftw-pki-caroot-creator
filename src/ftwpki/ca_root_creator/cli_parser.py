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

from pathlib import Path
from typing import TypeAlias

from ftwpki.baselibs._cli_parser import (
    _HELP,
    DistinguishedNameArguments,
    load_help_entries,
    parser_factory_creator,
)

HELP_FILE = Path(__file__).parent.joinpath("cli_parser.help")


load_help_entries(_HELP, HELP_FILE)

# print(MY)


LANG="en"

class CaInitArguments(DistinguishedNameArguments):
    """
    Class for Root-CA initialization arguments.
    """
    __slots__ = ["passphrasefile", "conf_file", "key_name", "certificate"]
    helpid = ["rootca"]
    arg_data = {
        "passphrasefile": {"flags": [], "kws": {}, "pre": {"nargs": "?"}},
        "conf_file": {"flags": [], "kws": {}, "pre": {"nargs": "?"}},
        "key_name": {"flags": ["-k", "--key", "--key-name"], "kws": {"default": ""}, "pre": {}},
        "certificate": {
            "flags": ["-c", "--cert", "--certificate"],
            "kws": {"default": ""},
            "pre": {},
        },
    }

    def __init__(self) -> None:
        """
        Initialize the Root-CA argument container with empty values.
        """
        super().__init__()
        self.passphrasefile:str=""
        self.conf_file:str=""
        self.key_name:str=""
        self.certificate:str=""


"""
Type alias for the Root-CA initialization argument container.
"""
CaInit: TypeAlias = CaInitArguments

ca_init_parser = parser_factory_creator(CaInitArguments)
"""
Factory function for creating Root-CA initialization parsers.

:type: Callable
"""




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
        # "test_new_parser.rst",
          "get_started_cli_parser.rst",
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
