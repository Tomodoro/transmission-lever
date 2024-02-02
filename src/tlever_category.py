#!/usr/bin/env python

import os
from tlever_label import mk_label, rm_label
from tlever_torrent import mv_data
from tlever_client import get_downloads_dir, get_client


def category_prefix(config) -> str:

    """
    Returns the category prefix from configration file
    :param config: valid configuration dictionary
    :return: category prefix
    """

    return config['General']['prefix']['categories']


def mk_category(config: dict,
                torrent_hash: str,
                category_name: str
                ) -> None:

    """
    Create an emulated category through labels
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :param category_name: name of the category
    :return: None
    """

    client = get_client(config)

    label = category_prefix(config) + category_name
    mk_label(client, torrent_hash, label)

    directory = os.path.join(get_downloads_dir(client), category_name)
    mv_data(client, torrent_hash, directory)

    return


def rm_category(config: dict,
                torrent_hash: str,
                category_name: str
                ) -> None:

    """
    Delete an emulated category through labels
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :param category_name: name of the category
    :return: None
    """

    client = get_client(config)

    directory = get_downloads_dir(client)
    mv_data(client, torrent_hash, directory)

    label = category_prefix(config) + category_name
    rm_label(client, torrent_hash, label)

    return
