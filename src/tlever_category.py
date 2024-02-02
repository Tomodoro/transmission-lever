#!/usr/bin/env python

import logging
from transmission_rpc import Client
from tlever_label import *
from tlever_directory import *


def category_prefix() -> str:
    return "@"


def downloads_path() -> str:
    return "/var/lib/transmission/Downloads"


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

    directory = os.path.join(downloads_path(), category_name)
    mk_directory(directory)

    label = category_prefix() + category_name
    mk_label(client, torrent_hash, label)

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

    client.change_torrent(ids=[torrent_hash], location=downloads_path())

    directory = os.path.join(downloads_path(), category_name)
    rm_directory(directory)

    label = category_prefix() + category_name
    rm_label(client, torrent_hash, label)

    return
