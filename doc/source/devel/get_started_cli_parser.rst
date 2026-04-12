

>>> from ftwpki.ca_root.cli_parser import CaInitParser

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
    private_key=None, 
    public_key=None, 
    privatdir=None)

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
    private_key=None, 
    public_key=None, 
    privatdir=None)

>>> from ftwpki.ca_root.cli_parser import CaSignParser

>>> csp = CaSignParser()
>>> csp #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
CaSignParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)
