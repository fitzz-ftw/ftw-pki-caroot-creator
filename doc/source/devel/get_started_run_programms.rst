The Certificat Authority Root Creation
#########################################



.. SECTION - Setup

>>> test_data_pre= "test_ok_data"

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)

.. !SECTION
.. SECTION - Prepare

>> print(f"{test_data_pre}/carootsecret")

>>> test_paswd_path = env.copy2cwd(f"{test_data_pre}/carootsecret", "carootsecret")

>>> conf_file = env.copy2cwd(f"{test_data_pre}/ca_root_conf.toml", "ca_root.toml")

>>> def stub_getpasswd(prompt:str)->str:
...     print(prompt)
...     return "secret"

>>> from ftwpki.ca_root_creator.programms import getpass

>>> getpass.getpass = stub_getpasswd

>>> cmd_line = " -k caroot  --cert caroot.cert.pem "
>>> cmd_line += " carootsecret "
>>> cmd_line +=" ca_root.toml "

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['-k', 'caroot', '--cert', 'caroot.cert.pem', 'carootsecret', 'ca_root.toml']

..!SECTION

>>> from ftwpki.ca_root_creator.programms import prog_ca_root_creator_cert

>>> prog_ca_root_creator_cert(sys_argv)
Enter Passphrase:
0


>>> prog_ca_root_creator_cert(sys_argv)
[Errno 2] No such file or directory: 'ca_root.toml'
1

>>> env.clean_home()
>>> env.clean_output()

>>> test_paswd_path = env.copy2cwd(f"{test_data_pre}/carootsecret", "carootsecret")

>>> conf_file = env.copy2cwd(f"{test_data_pre}/ca_root_conf.toml", "ca_root.toml")



>>> def stub_keyboard_interrupt(prompt:str):
...     print(prompt)
...     raise KeyboardInterrupt
...     return ""

>>> getpass.getpass = stub_keyboard_interrupt
>>> prog_ca_root_creator_cert(sys_argv)
Enter Passphrase:
1


.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION
