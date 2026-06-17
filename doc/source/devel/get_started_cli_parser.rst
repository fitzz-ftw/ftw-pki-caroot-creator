Comand Line Parser
###################

>>> from ftwpki.ca_root_creator.cli_parser import ca_init_parser

>>> cip = ca_init_parser()
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



>>> from ftwpki.ca_root_creator.cli_parser import ca_init_parser

>>> ca_init_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> cip = ca_init_parser(add_help=False)
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=False)
