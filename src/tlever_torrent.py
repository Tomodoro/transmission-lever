#!/usr/bin/env python

import os
import logging
from transmission_rpc import Client, Torrent
from tlever_client import get_downloads_dir
from tlever_structures import TorrentStub


def mv_data(client: Client,
            torrent_hash: str,
            directory: str
            ) -> None:

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


def get_stub_info(client: Client,
                  torrent_hash: str,
                  prefixes: dict
                  ) -> TorrentStub:
    """
    Get subset of info from a torrent
    :param prefixes: dictionary of label prefixes
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :return: object with stub info
    """

    torrent = client.get_torrent(torrent_id=torrent_hash)

    #
    # separate tier/cat/tag labels
    #
    tier, category, tag = None, None, ''
    for label in torrent.labels:

        if label[0] == prefixes['tier']:  # found tier
            tier = int(label[5:])

        elif label[0] == prefixes['category']:  # found category
            category = label[1:]

        elif label[0] == prefixes['tag']:  # found tag
            if tag != '':
                tag = tag + ', ' + label[1:]
            else:
                tag = label[1:]

    #
    # ETA in words
    #
    if torrent.eta == -1:
        eta = 'Not Available'
    elif torrent.eta == -2:
        eta = 'Unknown'
    else:
        eta = torrent.eta

    #
    # set ratio
    #
    global_ratio_limit = client.get_session().seed_ratio_limit

    if torrent.seed_ratio_mode == 0:
        pretty_ratio_limit = "[{}] (Global)".format(global_ratio_limit)
    elif torrent.seed_ratio_mode == 1:
        pretty_ratio_limit = "[{}]".format(torrent.seed_ratio_limit)
    else:
        pretty_ratio_limit = '[Unlimited]'

    ratio_pretty = "{} {}".format(torrent.ratio, pretty_ratio_limit)

    def format_bytes(size):

        """
        Format bytes size to use metric prefix
        :param size: bytes
        :return: two values: reduced size and metric prefix
        """

        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: 'B/s', 1: 'KiB/s', 2: 'MiB/s', 3: 'Gib/s', 4: 'TiB/s'}
        while size > power:
            size /= power
            n += 1
        return int(size), power_labels[n]

    def pretty_metric(is_limited: bool,
                      speed: int,
                      limit: int
                      ) -> str:

        """
        Return prettified speed and limit with metric prefix
        :param is_limited: if the speed is limited
        :param speed: the value of the speed in bytes
        :param limit: the value of the limit in bytes
        :return:
        """

        if is_limited:
            metric_limit = format_bytes(limit)
            metric_speed = format_bytes(speed)

            return "{} {} [{} {}]".format(metric_speed[0],
                                          metric_speed[1],
                                          metric_limit[0],
                                          metric_limit[1])

        else:
            return "[Global]"

    up_pretty = pretty_metric(torrent.upload_limited,
                              torrent.rate_upload,
                              torrent.upload_limit)

    down_pretty = pretty_metric(torrent.download_limited,
                                torrent.rate_download,
                                torrent.download_limit)

    output = TorrentStub(
        name=torrent.name,
        hash=torrent.hashString,
        ratio=torrent.ratio,
        ratio_limit=torrent.seed_ratio_limit,
        ratio_limit_mode=torrent.seed_ratio_mode,
        ratio_pretty=ratio_pretty,
        progress=torrent.progress,
        group=torrent.group,
        tier=tier,
        category=category,
        tag=tag,
        eta=eta,
        up_speed_bytes=torrent.rate_upload,
        up_limit_bytes=torrent.upload_limit,
        up_limit_state=torrent.download_limited,
        up_pretty=up_pretty,
        down_speed_bytes=torrent.rate_download,
        down_limit_bytes=torrent.download_limit,
        down_limit_state=torrent.upload_limited,
        down_pretty=down_pretty
    )

    return output


def get_abs_download_dir(torrent: Torrent) -> str:

    """
    Get the absolute path directory of torrent
    :param torrent: torrent object
    :return: absolute path of a torrent
    """

    return torrent.download_dir


def get_rel_download_dir(client: Client,
                         torrent: Torrent
                         ) -> str:

    """
    Get the relative path directory of torrent
    :param client: valid transmission session
    :param torrent: torrent object
    :return: relative path of a torrent
    """

    full_path = get_abs_download_dir(torrent)
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
                          seed_ratio_limit=limits["seed_ratio_limit"],
                          upload_limit=limits["upload_limit"],
                          upload_limited=limits["upload_limited"])
