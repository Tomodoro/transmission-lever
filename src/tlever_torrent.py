#!/usr/bin/env python

import os
import logging
from transmission_rpc import Client, Torrent
from tlever_client import get_downloads_dir


def mv_data(client: Client,
            torrent_hash: str,
            directory: str) -> None:

    """
    Move data of a torrent
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param directory: directory where to move the data
    :return: None
    """

    old_directory = client.get_torrent(torrent_id=torrent_hash).download_dir
    logging.info(f"Moving data from {old_directory} to {directory} for torrent with hash {torrent_hash}")
    client.move_torrent_data(ids=[torrent_hash], location=directory)
    return None


def get_torrent_abs_download_dir(torrent: Torrent) -> str:

    """
    Get the absolute path directory of torrent
    :param torrent: torrent object
    :return: absolute path of a torrent
    """

    return torrent.download_dir


def get_torrent_rel_download_dir(client: Client,
                                 torrent: Torrent) -> str:

    """
    Get the relative path directory of torrent
    :param client: valid transmission session
    :param torrent: torrent object
    :return: relative path of a torrent
    """

    full_path = get_torrent_abs_download_dir(torrent)
    base_path = get_downloads_dir(client)

    rel_path = os.path.relpath(full_path, base_path)

    if rel_path == '.':
        return ''
    else:
        return str(rel_path)


def change_upload_throttle(client,
                           torrent_hash: str,
                           limits: dict
                           ) -> None:

    """
    Change upload throttle of a torrent
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param limits: dictionary with upload limits
    :return:
    """

    client.change_torrent(ids=[torrent_hash],
                          seed_idle_limit=limits['seed_idle_limit'],
                          seed_idle_mode=limits["seed_idle_mode"],
                          seed_ratio_mode=limits["seed_ratio_mode"],
                          upload_limit=limits["upload_limit"],
                          upload_limited=limits["upload_limited"])
