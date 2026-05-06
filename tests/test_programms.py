



from ftwpki.ca_root.programms import prog_ca_root_cert


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

