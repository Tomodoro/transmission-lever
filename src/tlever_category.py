#!/usr/bin/env python

import logging
from transmission_rpc import Client
from tlever_label import *
from tlever_directory import *


def category_prefix() -> str:
    return "@"


def downloads_path(client) -> str:
    return client.get_session().download_dir


def mk_category(client: Client,
                torrent_hash: str,
                category_name: str
                ) -> None:

    """
    Create an emulated category through labels
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param category_name: name of the category
    :return: None
    """

    label = category_prefix() + category_name
    mk_label(client, torrent_hash, label)

    directory = os.path.join(downloads_path(client), category_name)
    client.move_torrent_data(ids=[torrent_hash], location=directory)

    return


def rm_category(client: Client,
                torrent_hash: str,
                category_name: str
                ) -> None:

    """
    Delete an emulated category through labels
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param category_name: name of the category
    :return: None
    """

    directory = downloads_path(client)
    client.move_torrent_data(ids=[torrent_hash], location=directory)

    label = category_prefix() + category_name
    rm_label(client, torrent_hash, label)

    return
