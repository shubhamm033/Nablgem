import argparse
import getpass
import logging
import os
import sys
import traceback
import pkg_resources

from colorlog import ColoredFormatter
from userregistration_client  import registration,mnemonic,recover_child_keys,recover_master_keys

DISTRIBUTION_NAME = 'User registration'

DEFAULT_URL = 'http://localhost:8008'

def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)
    clog.setLevel(logging.DEBUG)
    
    return clog

def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))

def registration_parser(subparsers,parent_parser):
    
    parser = subparsers.add_parser(
        'registration',
        help='register a new user',
        parents=[parent_parser])

    parser.add_argument(
        'email',
        type=str,
        help='email of the user')

    parser.add_argument(
        'phonenumber',
        type=str,
        help='phone number of the user')


def mnemonic_parser(subparsers,parent_parser):

    parser = subparsers.add_parser(
        'mnemonic',
        help='register a new user',
        parents=[parent_parser])

    parser.add_argument(
        'email',
        type=str,
        help='email of the user')

    parser.add_argument(
        'phonenumber',
        type=str,
        help='phone number of the user')

    parser.add_arguement(
        'password',
        type = str,
        help = "password"
    )

def master_key_parser(subparsers,parent_parser):

    parser = subparsers.add_parser(
        'master key',
        help='master key of the registered user',
        parents=[parent_parser])

    parser.add_argument(
        'mnemonic',
        type=str,
        help='mnemonic of the user')

def child_key_parser(subparser,parent_parser):

    parser =subparsers.add_parser(
        'child key',
        help = "child key of the user",
        parents =[parent_parser]
    )
    
    parser.add_arguement(
        'mnemonic',
        type =str,
        help= 'mnemonic of the user'
    )

    parser.add_arguement(
     'index',
     type = int,
     help = "index of the child key"
     )


def create_parent_parser(prog_name):
    '''Define the -V/--version command line options.'''
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='display version information')

    return parent_parser


def create_parser(prog_name):
    '''Define the command line parsing for all the options and subcommands.'''
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands to manage your simple wallet',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    registration_parser(subparsers, parent_parser)
    mnemonic_parser(subparsers, parent_parser)
    master_key_parser(subparsers, parent_parser)
    child_key_parser(subparsers, parent_parser)

    return parser
    
def _get_keyfile(customerName):
    '''Get the private key for a customer.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, customerName)

def _get_pubkeyfile(customerName):
    '''Get the public key for a customer.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.pub'.format(key_dir, customerName)

def do_registration(args):
    '''Implements the "deposit" subcommand by calling the client class.'''

    

    print ("Here are the values")
    password, user_id = registration(args.email, args.phone_number)

    if password:
        print("Your User ID is : {}".format(user_id))
        print ("Please note down your password carefully, This password is mandatory to do any transaction")
        print("Your Password is : {}".format(password))
    else:
        print ("You already have been registered with %s"%args.email)


def recover_mnemonic(args):
    _mnemonic = mnemonic(args.email, args.phone_number, args.password)
    print (_mnemonic)

def master_keys(args):
    private_key, public_key = recover_master_keys(args.mnemonic)
    print("Your Master Private key is : {}".format(private_key))
    print("Your Master Public key is : {}".format(public_key))


def child_keys(args):
    private_key, public_key = recover_child_keys(args.mnemonic, args.index)
    print("Your Child Private key at index {} is : {}".format(args.index, private_key))
    print("Your Child Public key at index {} is : {}".format(args.index, public_key))

def main(prog_name=os.path.basename(sys.argv[0]), args=None):
    '''Entry point function for the client CLI.'''
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(prog_name)
    args = parser.parse_args(args)

    verbose_level = 0

    setup_loggers(verbose_level=verbose_level)

    # Get the commands from cli args and call corresponding handlers
    if args.command == 'deposit':
        do_deposit(args)
    elif args.command == 'withdraw':
        do_withdraw(args)
    elif args.command == 'balance':
        do_balance(args)
    elif args.command == 'masterkeys':
        master_keys(args)
    elif args.command == 'childkeys':
            child_keys(args)
    elif args.command == 'mnemonic':
        recover_mnemonic(args)
    elif args.command == 'registration':
        do_registration(args)

        
    elif args.command == 'transfer':
        # Cannot deposit and withdraw from own account. noop.
        if args.customerNameFrom == args.customerNameTo:
            raise Exception("Cannot transfer money to self: {}"
                                        .format(args.customerNameFrom))

        do_transfer(args)
    else:
        raise Exception("Invalid command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ =="__main__":
    main_wrapper()

