import logging
from korbit.client.korbit_client import KorbitClient

logging.basicConfig(level=logging.INFO)

properties_sandbox_file = '../properties_sandbox_test.json'
context_sandbox_file = '../context_sandbox.json'

kbclient = KorbitClient(properties_sandbox_file, context_sandbox_file)

kbclient._refreshAccessToken()