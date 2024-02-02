#!/usr/bin/env python

import sys
import logging
from transmission_rpc import Client


def get_client(config: dict) -> Client:

    """
    Get a transmission RPC client
    :param config: valid configuration dictionary
    :return: transmission session
    """

    try:
        client = Client(host=config["Client"]["host"],
                        port=int(config["Client"]["port"]),
                        username=config["Client"]["username"],
                        password=config["Client"]["password"])
        return client

    except:
        logging.error("Authorization failed")
        sys.exit()


def get_rpc_semver(client: Client) -> str:

    """
    Get RPC server version
    :param client: valid transmission session
    :return: version of the RPC server
    """

    return client.get_session().rpc_version_semver


def get_transmission_version(client: Client) -> str:

    """
    Get transmission server version
    :param client: valid transmission session
    :return: version of the transmission server
    """

    return client.get_session().version


def get_downloads_dir(client: Client) -> str:

    """
    Get global download directory of transmission
    :param client: valid transmission session
    :return: global download directory
    """

    return client.get_session().download_dir
