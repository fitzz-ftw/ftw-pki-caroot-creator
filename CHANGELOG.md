# Changelog - ftw-pki-ca-root-creator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.0.3a1] - 2026-05-14

### Added
- First release with the new name `ftw-pki-ca-root-creator`.
- Added logic for Root CA management in `caroot.py`.
- Added CLI tool `ftwpkicaroot` to create a Root CA.
- Reached 100% test coverage for Python 3.11 to 3.15.

### Changed
- **Major Refactoring:** Renamed the package from `ca-root` to `ca-root-creator`.
- **Namespace Migration:** Changed all imports from `ftwpki.ca_root` to `ftwpki.ca_root_creator`.
- Removed `platformdirs` from the main dependencies.
- Now using `pathlib` for all file and directory tasks.

## [0.0.2] - 2026-02-15

### Added
- Added API documentation for all modules (`caroot`, `cli_parser`, `programms`, `protocols`).
- Integrated Sphinx rules for automatic documentation.
- First stable version of the core CA protocols.

## [0.0.1] - 2025-11-20

### Added
- Initial commit and project structure.
