#!/usr/bin/env python

import logging
from transmission_rpc import Client


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
