import argparse
import asyncio
import logging
import os
from signal import signal, SIGINT
import sys

import rethinkdb as r

from sanic import Sanic,request

from sawtooth_signing import create_context
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing import CryptoFactory

from sawtooth_rest_api.messaging import Connection

from zmq.asyncio import ZMQEventLoop

from api.accounts import ACCOUNTS_BP
from api.assets import ASSETS_BP
from api.authorization import AUTH_BP
from api.errors import ERRORS_BP
# from api.holdings import HOLDINGS_BP
# from api.offers import OFFERS_BP


LOGGER = logging.getLogger(__name__)
DEFAULT_CONFIG = {
    'HOST': 'localhost',
    'PORT': 8000,
    'TIMEOUT': 500,
    'VALIDATOR_URL': 'tcp://localhost:4004',
    'DB_HOST': 'localhost',
    'DB_PORT': 28015,
    'DB_NAME': 'main_db',
    'DEBUG': True,
    'KEEP_ALIVE': False,
    'SECRET_KEY': None,
    'AES_KEY': None,
    'BATCHER_PRIVATE_KEY': None,
    "REST_API_URL":"http://127.0.0.1:8008",
    "TIMEOUT": 60,
    "ROOT_KEY_INDEX": 0,
    "BUCKET_NAME": "personal-demo-bucket"
    
}



async def open_connections(app):
    LOGGER.warning('opening database connection')
    r.set_loop_type('asyncio')
    app.config.DB_CONN = await r.connect(
        host=app.config.DB_HOST,
        port=app.config.DB_PORT,
        db=app.config.DB_NAME)
    # print(app.config.DB_NAME)

    # app.config.VAL_CONN = Connection(app.config.VALIDATOR_URL)
    # print(app.config.VAL_CONN)
    # LOGGER.warning('opening validator connection')
    # app.config.VAL_CONN.open()
    

def close_connections(app):
    LOGGER.warning('closing database connection')
    app.config.DB_CONN.close()

    LOGGER.warning('closing validator connection')
    app.config.VAL_CON.close()


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='The host for the api to run on.')
    parser.add_argument('--port',
                        help='The port for the api to run on.')
    parser.add_argument('--timeout',
                        help='Seconds to wait for a validator response')
    parser.add_argument('--validator',
                        help='The url to connect to a running validator')
    parser.add_argument('--db-host',
                        help='The host for the state database')
    parser.add_argument('--db-port',
                        help='The port for the state database')
    parser.add_argument('--db-name',
                        help='The name of the database')
    parser.add_argument('--debug',
                        help='Option to run Sanic in debug mode')
    parser.add_argument('--secret_key',
                        help='The API secret key')
    parser.add_argument('--aes-key',
                        help='The AES key used for private key encryption')
    parser.add_argument('--batcher-private-key',
                        help='The sawtooth key used for transaction signing')
    parser.add_argument('--aws-access-key',
                        help='The aws access key used for file uploading')
    parser.add_argument('--aws-secret-key',
                        help='The aws secret key used for file uploading')                    
    return parser.parse_args(args)




def load_config(app):  # pylint: disable=too-many-branches
    app.config.update(DEFAULT_CONFIG)
    config_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'config.py')
    try:
        app.config.from_pyfile(config_file_path)
    except FileNotFoundError:
        LOGGER.warning("No config file provided")

    # CLI Options will override config file options
    opts = parse_args(sys.argv[1:])

    if opts.host is not None:
        app.config.HOST = opts.host
    if opts.port is not None:
        app.config.PORT = opts.port
    if opts.timeout is not None:
        app.config.TIMEOUT = opts.timeout

    if opts.validator is not None:
        app.config.VALIDATOR_URL = opts.validator
    if opts.db_host is not None:
        app.config.DB_HOST = opts.db_host
    if opts.db_port is not None:
        app.config.DB_PORT = opts.db_port
    if opts.db_name is not None:
        app.config.DB_NAME = opts.db_name

    if opts.debug is not None:
        app.config.DEBUG = opts.debug

    if opts.secret_key is not None:
        app.config.SECRET_KEY = opts.secret_key
    if app.config.SECRET_KEY is None:
        LOGGER.exception("API secret key was not provided")
        sys.exit(1)

    if opts.aes_key is not None:
        app.config.AES_KEY = opts.aes_key
    if app.config.AES_KEY is None:
        LOGGER.exception("AES key was not provided")
        sys.exit(1)
    
    if opts.batcher_private_key is not None:
        app.config.BATCHER_PRIVATE_KEY = opts.batcher_private_key
    if app.config.BATCHER_PRIVATE_KEY is None:
        LOGGER.exception("Batcher private key was not provided")
        sys.exit(1)
    try:
        private_key = Secp256k1PrivateKey.from_hex(
            app.config.BATCHER_PRIVATE_KEY)
    except ParseError as err:
        LOGGER.exception('Unable to load private key: %s', str(err))
        sys.exit(1)
    app.config.CONTEXT = create_context('secp256k1')
    app.config.SIGNER = CryptoFactory(
        app.config.CONTEXT).new_signer(private_key)


def main():
    app = Sanic(__name__)
    app.blueprint(ACCOUNTS_BP,url_prefix='/accounts')
    app.blueprint(ASSETS_BP,url_prefix='/assets')

    # app.blueprint(AUTH_BP)
    # app.blueprint(ERRORS_BP)
    # app.blueprint(HOLDINGS_BP)
    
    # app.blueprint(OFFERS_BP)
    
    load_config(app)
    # open_connections(app)
    # app.run(host='0.0.0.0', port=8000, debug=True)
    zmq = ZMQEventLoop()
    asyncio.set_event_loop(zmq)
    server = app.create_server(
        host=app.config.HOST, port=app.config.PORT, debug=True)
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(server)
    asyncio.ensure_future(open_connections(app))
    
    signal(SIGINT, lambda s, f: loop.close())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        close_connections(app)
        loop.stop()

if __name__ =="__main__":
    main()



