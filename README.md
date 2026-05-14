# ftw-pki-caroot-creator

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
[![Coverage: 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)]

The authoritative Root Certificate Authority (Root CA) creation tool of the **ftw-pki** suite. This repository provides the `ftwpkicaroot` executable, specifically designed for the initial generation of the Root CA.

## 🛠 Features

* **Root CA Initialization:** Dedicated logic to generate the ultimate anchor of trust for the entire PKI infrastructure.
* **Security-First Lifecycle:** Designed as a temporary tool. Once the Root CA is established, this program should be decommissioned to minimize the system's attack surface.
* **Hardened Passphrase Support:** Works in conjunction with `ftw-pki-password` to handle high-entropy passphrases (~80+ characters).
* **Standard Compliance:** Generates X.509 root certificates following strict security profiles.

## 📖 Documentation & Usage

**Note on Security:** This program is intended for the creation of the Root CA only. For ongoing signing operations, a separate, dedicated signing tool is used.

* **Usage:** The `ftwpkicaroot` utility handles the lifecycle of the Root CA's initial setup. Run `ftwpkicaroot --help` for available commands.
* **Post-Setup Recommendation:** After successfully creating and backing up the Root CA, it is highly recommended to uninstall this package and remove the executable from the environment.
* **Technical Manual:** Detailed security considerations and operational guides are located in the `doc/source/` directory.

## 📄 License

This project is licensed under the **LGPL v2.1 (or later)**.

---
© 2026 ftw-pki Contributors
