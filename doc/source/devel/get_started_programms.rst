The Certificat Authority Root Creation
#########################################



.. SECTION - Setup

>>> test_data_pre= "data-root-creator"

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)

.. !SECTION
.. SECTION - Prepare

>> print(f"{test_data_pre}/carootsecret")

>>> test_paswd_path = env.copy2cwd(f"{test_data_pre}/carootsecret", "carootsecret")

>>> conf_file = env.copy2cwd(f"{test_data_pre}/ca_root_conf.toml", "ca_root.toml")

>>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "secret"

>>> cmd_line = " -k caroot  --cert caroot.cert.pem "
>>> cmd_line += " carootsecret "
>>> cmd_line +=" ca_root.toml "

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['-k', 'caroot', '--cert', 'caroot.cert.pem', 'carootsecret', 'ca_root.toml']

..!SECTION

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn
>>> from ftwpki.ca_root_creator.cli_parser import ca_init_parser

>>> pki_file: Path|None = None

>>> pre_parser = ca_init_parser(prog="ftwpkicaroot", add_help=False, allow_abbrev=False)
>>> pre_args , _ = pre_parser.parse_known_args(sys_argv)
>>> ca_parser = ca_init_parser(prog="ftwpkicaroot")
>>> pre_conf = toml2dn(Path(pre_args.conf_file).read_text())

>>> ca_parser.set_defaults(**pre_conf)

>>> del pre_parser

>>> args = ca_parser.parse_args(sys_argv)
>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS 
CaInitArguments(certificate='caroot.cert.pem'
    commonName='Muster-Verband Bundesverband Root CA'
    conf_file='ca_root.toml'
    countryName='DE'
    dnsubject={'countryName': 'DE', 
        'localityName': 'Berlin', 
        'organizationName': 'Muster-Verband e.V.', 
        'organizationalUnitName': 'Zentraler PKI-Dienst', 
        'commonName': 'Muster-Verband Bundesverband Root CA'}
    key_name='caroot'
    localityName='Berlin'
    organizationName='Muster-Verband e.V.'
    organizationalUnitName='Zentraler PKI-Dienst'
    passphrasefile='carootsecret'
    stateOrProvinceName='')

>>> conf_file = Path(args.conf_file)
>>> pass_file = Path(args.passphrasefile)

.. !SECTION - Configuration

.. SECTION - Passwordhandling

>>> from ftwpki.baselibs.passwd import PasswordManager
>>> pwd_man = PasswordManager(private_dir='')
>>> pwd_man
PasswordManager(private_dir='.')

>>> password  = getpasswd("Enter Passphrase:")
Enter Passphrase:

.. !SECTION - Passwordhandling

.. SECTION - Certificatecreating

>>> from ftwpki.ca_root_creator.caroot import CertificateAuthority

>>> ca_root_creator = CertificateAuthority(
...     common_name = args.commonName,
...     country = args.countryName,
...     state = args.stateOrProvinceName,
...     location = args.localityName,
...     organization = args.organizationName,
...     organizational_unit = args.organizationalUnitName    
... )



>>> ca_root_creator.create_root_certificate(passphrase= pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = password
... ), days = 20*370)

>>> from ftwpki.baselibs.core import load_private_key_from_pem,load_certificate_from_pem

>>> private_key=load_private_key_from_pem(pem_data=ca_root_creator.private_key, 
...     passphrase=pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = password))

>>> del password

>>> cert_obj = load_certificate_from_pem(ca_root_creator.certificate)


.. SECTION - pki- Container

>>> from ftwpki.baselibs.package import PKIPackage

>>> pki_pack = PKIPackage()

>>> pki_pack.additional_files[str(conf_file.with_suffix(".policy").name)]=conf_file.read_bytes()
>>> pki_pack.additional_files[pass_file.name]=pass_file.read_bytes()
>>> pki_pack.message = pass_file.name
>>> pki_pack.additional_files["CA.key.pem"]=ca_root_creator.private_key


>>> pki_pack.recipient_cert=cert_obj
>>> pki_pack.caroot_cert=cert_obj




>>> pki_pack.private_key=private_key
>>> pki_pack.ca_cert=cert_obj

>>> pki_file = pki_pack.save(conf_file)

.. !SECTION - pki- Container

.. SECTION - Cleanup CWD

>>> conf_file.unlink()

>>> pass_file.unlink()

.. !SECTION - Cleanup CWD

>>> pki_file.is_file()
True

.. !SECTION - End programm

.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION
