# File: src/ftwpki/ca_root/protocols.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
protocols
===============================

Structural interfaces for the Root-CA management package. (ro)
"""

from pathlib import Path

from ftwpki.baselibs.protocols import DistinguishedNameProtocol


# CLASS - CaInitProtocol
class CaInitProtocol(DistinguishedNameProtocol):
    """
    Structural interface for Root-CA initialization data. (ro)

    Extends DistinguishedNameProtocol to include all necessary file paths
    for creating a new Root Certificate Authority.
    """

    public_key: str
    """Filename for the generated public key/certificate."""
    private_key: str
    """Filename for the generated encrypted private key."""
    privatdir: str
    """Path to the directory where private keys are stored."""
    passphrasefile: str
    """Filename of the encrypted passphrase secret."""
    certificate: str
    """Filename for the self-signed root certificate."""


# !CLASS - CaInitProtocol


# CLASS - CaSignProtocol
class CaSignProtocol(DistinguishedNameProtocol):
    """
    Structural interface for Root-CA signing operations. (ro)

    Defines the required attributes to access the Root-CA's private
    infrastructure for signing requests.
    """

    private_key: str
    """Filename of the Root-CA private key to be used for signing."""
    privatdir: str
    """Path to the directory containing the private key."""


# !CLASS - CaSignProtocol


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
    test_file = testfiles_dir / "get_started_protocols.rst"

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
