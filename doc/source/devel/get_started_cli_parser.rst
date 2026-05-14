Comand Line Parser
###################

>>> from ftwpki.ca_root_creator.cli_parser import CaInitParser

>>> cip = CaInitParser()
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
CaInitParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> cip.parse_args(["passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
Namespace(countryName='', 
    stateOrProvinceName='', 
    localityName='', 
    organizationName='', 
    organizationalUnitName='', 
    commonName='', 
    dnsubject={}, 
    conf_file=None, 
    passphrasefile='passwort.txt', 
    private_key='', 
    certificate='',
    public_key='', 
    privatdir='')

>>> cip.parse_args(["-subj", "/CN=Test" ,"passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
Namespace(countryName='', 
    stateOrProvinceName='', 
    localityName='', 
    organizationName='', 
    organizationalUnitName='', 
    commonName='Test', 
    dnsubject={'commonName': 'Test'}, 
    conf_file=None, 
    passphrasefile='passwort.txt', 
    private_key='',
    certificate='', 
    public_key='', 
    privatdir='')



>>> from ftwpki.ca_root_creator.cli_parser import get_ca_init_parser

>>> get_ca_init_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
CaInitParser(prog='ftwpkicaroot', 
    usage=None, 
    description='Initialize a Root-CA with specified parameters.', 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)
