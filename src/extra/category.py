#!/usr/bin/env python

import os

from core.label import mk_label, rm_label, find_regex_label
from core.torrent import mv_data, get_rel_download_dir
from core.client import get_downloads_dir, get_client, get_torrents_list


def category_prefix(config) -> str:

    """
    Returns the category prefix from configration file
    :param config: valid configuration dictionary
    :return: category prefix
    """

    return config['General']['prefix']['categories']


def category_exists(config: dict,
                    target: str
                    ) -> bool:
    """
    Checks if the category exists in the configuration
    :param target: category to check
    :param config: valid configuration dictionary
    :return: True if category exists, False otherwise
    """

    category_list = config["General"]["categories"]

    for category in category_list:
        if category == target:
            return True
    return False


def category_directory(config: dict,
                       target: str
                       ) -> str:
    """
    Returns the category directory from configration file
    :param config: valid configuration dictionary
    :param target: category to search directory
    :return: Path of category if exists, root directory otherwise
    """

    client = get_client(config)
    root_dir = get_downloads_dir(client)

    category_list = config["General"]["categories"]

    for category in category_list:
        if category == target:
            return os.path.join(root_dir, config["Categories"][category])
    return root_dir


def enforce_categories(config: dict) -> None:

    """
    Syncs torrent data dir with category label
    :param config: valid configuration dictionary
    :return: None
    """

    client = get_client(config)

    # For every torrent in the torrent list
    for torrent in get_torrents_list(client):

        # We get the torrent relative download directory
        rel_torrent_dir = get_rel_download_dir(client, torrent)
        # We check that there is a category label
        label_exists = find_regex_label(client, torrent.hashString, "@")

        # If the category label exists
        if label_exists:

            # We grab all the torrent labels
            torrent_labels = torrent.labels

            # For every torrent label
            for label in torrent_labels:

                # We check for @ as the first char
                if label[0] == '@':

                    # We get the label relative directory
                    rel_label_dir = label.replace('@', '')

                    # If label rel dir does not equals torrent rel dir
                    if rel_torrent_dir != rel_label_dir:

                        # We enforce the category label directory
                        base_dir = get_downloads_dir(client)
                        final_dir = os.path.join(base_dir, rel_label_dir)
                        mv_data(client, torrent.hashString, final_dir)


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


def ls_category(config: dict) -> None:
    """
    List all emulated categories through labels
    :param config: valid configuration dictionary
    :return: list of category names
    """

    category_list = config["General"]["categories"]

    for category in category_list:
        category_path = config["Categories"][category]
        print(f"{category}: {category_path}")

    return
