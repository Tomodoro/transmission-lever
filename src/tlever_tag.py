#!/usr/bin/env python

import logging
from transmission_rpc import Client
from tlever_label import find_label, mk_label, rm_label


def tag_prefix() -> str:
    return '#'


def mk_tag(client: Client,
           torrent_hash: str,
           tag_name: str) -> bool:

    """
    Add a tag on a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param tag_name: name if the tag
    :return: True if the tag is created, False if it already exists
    """

    tag = tag_prefix() + tag_name
    return mk_label(client, torrent_hash, tag)


def rm_tag(client: Client,
           torrent_hash: str,
           tag_name: str) -> bool:

    """
    Remove a tag from a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param tag_name: name of the tag
    :return: True if the tag is removed, False if it does not exist
    """

    tag = tag_prefix() + tag_name
    return rm_label(client, torrent_hash, tag)

