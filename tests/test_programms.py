

import shlex
from pathlib import Path
from unittest.mock import patch

import pytest

from ftwpki.ca_root.programms import prog_ca_root_cert, prog_ca_root_singing


def test_prog_ca_root_cert_full_coverage(mocker, tmp_path):
    # 1. getpass patchen (jetzt wo du 'import getpass' nutzt)
    # Falls du 'from getpass import getpass' nutzt: "ftwpki.ca_root.programms.getpass"
    # Falls du 'import getpass' nutzt: "getpass.getpass"
    mock_getpass = mocker.patch("getpass.getpass", return_value="strenggeheim")

    # 2. Mocks für Infrastructure
    mocker.patch("ftwpki.ca_root.programms.save_pem")
    mock_pwd_man = mocker.patch("ftwpki.ca_root.programms.PasswordManager")
    mock_pwd_man.return_value.decrypt_password_file.return_value = "entschluesselt"

    # 3. Valide Argumente (inklusive Country 'DE' für die Längen-Validierung)
    argv = [
        "--commonName",
        "Fitzz Test CA",
        "-C",
        "DE",  # Das behebt den "length must be 2" Fehler
        "-ST",
        "Mystate",
        "--privatdir",
        str(tmp_path),
        "dummy_pass_file",
    ]

    # Ausführung
    exit_code = prog_ca_root_cert(argv)

    # Falls es immer noch 1 ist, lassen wir uns den Fehler anzeigen
    assert exit_code == 0
    assert mock_getpass.call_count == 2



def test_prog_ca_root_cert_exception_handling(mocker):
    """Testet den try-except Block (Zeile 51-53) für 100% Coverage."""
    mocker.patch("ftwpki.ca_root.programms.CaInitParser", side_effect=RuntimeError("Boom"))

    # Das sollte die Exception fangen und 1 zurückgeben
    exit_code = prog_ca_root_cert([])
    assert exit_code == 1

# SECTION - Programm: Signing

@pytest.fixture
def ca_test_env(monkeypatch):
    # 1. Pfad zum realen Test-Verzeichnis (relativ zum Projekt-Root)
    # Wir stellen sicher, dass wir den Pfad korrekt auflösen
    project_root = Path(__file__).parent.parent
    testhome_path = project_root / "doc" / "source" / "devel" / "testhome"

    from fitzzftw.devtools.testinfra import TestHomeEnvironment

    env = TestHomeEnvironment(testhome_path)

    # 2. Setup ausführen (bereitet die Verzeichnisse am realen Ort vor)
    env.setup(True)

    # 3. In das Verzeichnis wechseln, das env.setup als CWD vorgesehen hat
    # Meistens ist das der 'testoutput' oder das 'testhome' selbst
    monkeypatch.chdir(env.base_dir)

    # 4. Dateien für den Testlauf bereitstellen
    env.copy2cwd("ca_root_conf.toml")
    Path("privat").mkdir(parents=True, exist_ok=True)
    env.copy2cwd("privat/testpasswd")
    env.copy2cwd("privat/ca.key.pem")
    env.copy2cwd("ca_public/ca.cert", "ca.cert")
    env.copy2cwd("Fitzz-TeXnik-WeltSomewherecity.csr")

    # Automatisierung des Passwort-Prompts
    monkeypatch.setattr("getpass.getpass", lambda _: "strenggeheim")

    # Den Test ausführen lassen
    yield env

    # 5. Aufräumen nach dem Test
    env.clean_home()
    env.teardown()

def test_prog_ca_root_singing_success(ca_test_env):
    """Szenario: Alles korrekt -> Return 0"""
    cmd = (
        "--conf-file ca_root_conf.toml -k privat/ca.key.pem "
        "--private-dir privat --policy-name intermediate "
        "-c ca.cert testpasswd Fitzz-TeXnik-WeltSomewherecity.csr"
    )

    argv = shlex.split(cmd)

    result = prog_ca_root_singing(argv)

    assert result == 0
    # Check ob das Zertifikat erstellt wurde
    assert Path("Fitzz-TeXnik-WeltSomewherecity.crt").exists()
    # Check ob Datenbank-Eintrag existiert
    assert Path("db/index.txt").exists()

def test_prog_ca_root_singing_success_dbdir_exists(ca_test_env):
    """Szenario: Alles korrekt -> Return 0"""
    cmd = (
        "--conf-file ca_root_conf.toml -k privat/ca.key.pem "
        "--private-dir privat --policy-name intermediate "
        "-c ca.cert testpasswd Fitzz-TeXnik-WeltSomewherecity.csr"
    )

    argv = shlex.split(cmd)
    # NEU: Das db-Verzeichnis manuell vorab anlegen,
    # um den Branch in Zeile 110 zu covern.
    Path("db").mkdir(parents=True, exist_ok=True)

    result = prog_ca_root_singing(argv)

    assert result == 0
    # Check ob das Zertifikat erstellt wurde
    assert Path("Fitzz-TeXnik-WeltSomewherecity.crt").exists()
    # Check ob Datenbank-Eintrag existiert
    assert Path("db/index.txt").exists()


def test_prog_ca_root_singing_validation_fail(ca_test_env):
    """Szenario: Policy-Verstoß (falsche DN) -> Return 1"""
    # Hier müsstest du ein CSR nutzen, das die Policy verletzt
    # Oder die Policy in der TOML kurzfristig via Code manipulieren
    # Beispiel: Wir setzen eine Policy, die 'Match' verlangt, aber das CSR hat andere Daten

    # (Simulierter fehlerhafter Aufruf oder manipulierte Config)
    # ... Logik für Return 1 ...

    with pytest.MonkeyPatch().context() as m:
        m.setattr("getpass.getpass", lambda _: "strenggeheim")

        cmd = (
            "--conf-file ca_root_conf.toml -k privat/ca.key.pem "
            "--private-dir privat -c ca.cert testpasswd "
            "Fitzz-TeXnik-WeltSomewherecity.csr"
        )

        result = prog_ca_root_singing(shlex.split(cmd))
        assert result == 1


VALID_ARGV = ["my_pass_file", "my_request.csr"]



def test_prog_ca_root_singing_exception():
    # Testet den harten Absturz (Return 2)
    with patch("ftwpki.ca_root.programms.CSRSigningParser") as mock_parser:
        # Wir lassen die Instanziierung des Parsers scheitern
        mock_parser.side_effect = Exception("Crash")

        result = prog_ca_root_singing(VALID_ARGV)
        assert result == 2
# !SECTION Programm: Signing
