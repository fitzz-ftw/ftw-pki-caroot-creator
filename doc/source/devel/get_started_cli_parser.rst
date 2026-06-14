Comand Line Parser
###################

>>> from ftwpki.ca_root_creator.cli_parser import CaInitParser

>>> cip = CaInitParser()
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> cip.parse_args(["passwort.txt", "test.pki"]) #doctest: +NORMALIZE_WHITESPACE
CaInitArguments(certificate=''
commonName=''
conf_file='test.pki'
countryName=''
dnsubject={}
key_name=''
localityName=''
organizationName=''
organizationalUnitName=''
passphrasefile='passwort.txt'
stateOrProvinceName='')

>>> cip.parse_args(["-subj", "/CN=Test" ,"passwort.txt", "test.pki"]) #doctest: +NORMALIZE_WHITESPACE
CaInitArguments(certificate=''
    commonName='Test'
    conf_file='test.pki'
    countryName=''
    dnsubject={'commonName': 'Test'}
    key_name=''
    localityName=''
    organizationName=''
    organizationalUnitName=''
    passphrasefile='passwort.txt'
    stateOrProvinceName='')



>>> from ftwpki.ca_root_creator.cli_parser import get_ca_init_parser

>>> get_ca_init_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog='ftwpkicaroot', 
    usage=None, 
    description='Initialize a Root-CA with specified parameters.', 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> cip = CaInitParser(run_setup=False)
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)
