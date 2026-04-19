



.. SECTION - Setup

>>> from fitzzftw.develtool.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path
>>> private_dir:Path = Path("privat")
>>> private_dir.mkdir(parents=True, exist_ok=True)
>>> test_paswd_path = env.copy2cwd("privat/testpasswd")
>>> conf_file = env.copy2cwd("ca_root_conf.toml")

>>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "strenggeheim"

>>> cmd_line="--conf_file ca_root_conf.toml -ST Mystate --commonName 'Fitzz CA Root' "
>>> cmd_line += " -k ca.key.pem -p ca.pub.pem --cert ca.cert"
>>> cmd_line += " --privatdir privat"
>>> cmd_line += " testpasswd"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf_file', 'ca_root_conf.toml', 
 '-ST', 'Mystate', 
 '--commonName', 'Fitzz CA Root',
 '-k', 'ca.key.pem',
 '-p', 'ca.pub.pem', 
 '--cert', 'ca.cert',
 '--privatdir', 'privat',
 'testpasswd']

..!SECTION

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn
>>> from ftwpki.ca_root.cli_parser import CaInitParser

>>> ca_parser = CaInitParser(prog="ftwpkicaroot")
>>> ca_parser.set_defaults(**toml2dn(sys_argv))
>>> args = ca_parser.parse_args(sys_argv)
>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS 
Namespace(countryName='DE', 
    stateOrProvinceName='Mystate', 
    localityName='Somewherecity', 
    organizationName='Fitzz TeXnik Welt', 
    organizationalUnitName='Security', 
    commonName='Fitzz CA Root', 
    dnsubject={'countryName': 'DE', 
        'stateOrProvinceName': 'Mystate', 
        'organizationName': 'Fitzz TeXnik Welt', 
        'commonName': 'Fitzz CA Root', 
        'localityName': 'Somewherecity', 
        'organizationalUnitName': 'Security'}, 
    conf_file=...Path('ca_root_conf.toml'), 
    passphrasefile='testpasswd', 
    private_key='ca.key.pem', 
    certificate='ca.cert', 
    public_key='ca.pub.pem', 
    privatdir='privat')

.. !SECTION - Configuration

.. SECTION - Passwordhandling

>>> from ftwpki.baselibs.passwd import PasswordManager
>>> pwd_man = PasswordManager(private_dir=args.privatdir)
>>> pwd_man
PasswordManager(private_dir='privat')

>>> from ftwpki.ca_root.caroot import CertificateAuthority

>>> ca_root = CertificateAuthority(
...     common_name = args.commonName,
...     country = args.countryName,
...     state = args.stateOrProvinceName,
...     location = args.localityName,
...     organization = args.organizationName,
...     organizational_unit = args.organizationalUnitName    
... )

>>> ca_root.generate_key_pair(passphrase=pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = getpasswd("Enter Passphrase:")
... ))
Enter Passphrase:

>>> from ftwpki.baselibs.core import save_pem
>>> save_pem(ca_root.private_key, 
...     Path(f"{args.privatdir}/{args.private_key}"), 
...     is_private=True)
>>> save_pem(ca_root.public_key, Path(f"{args.public_key}"), is_private=False)

>>> ca_root.create_root_certificate(passphrase= pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = getpasswd("Enter Passphrase:")
... ), days = 20*370)
Enter Passphrase:

>>> save_pem(ca_root.certificate, Path(f"{args.certificate}"), is_private=False)


..!SECTION - Passwordhandling

..!SECTION

.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()

.. !SECTION
