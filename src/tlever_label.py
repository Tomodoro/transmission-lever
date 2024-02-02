#!/usr/bin/env python

import logging
from transmission_rpc import Client


def find_label(client: Client,
               torrent_hash: str,
               label_name: str,
               ) -> bool:
    """
    Find a label on a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param label_name: name of the label
    :return: True if the label is found, False otherwise
    """

    torrent_labels = client.get_torrent(torrent_hash).labels

    for label in torrent_labels:
        if label == label_name:
            logging.info(f"Found label {label_name} in torrent with hash {torrent_hash}")
            return True

    logging.info(f"No label {label_name} in torrent with hash {torrent_hash}")
    return False


def mk_label(client: Client,
             torrent_hash: str,
             label_name: str
             ) -> bool:
    """
    Add a label on a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param label_name: name of the label
    :return: True if the label is created, False if it already exists
    """

    exists = find_label(client, torrent_hash, label_name)

    if not exists:
        torrent_labels = client.get_torrent(torrent_hash).labels
        torrent_labels.append(label_name)
        client.change_torrent(ids=[torrent_hash], labels=torrent_labels)
        logging.info(f"Added label {label_name} in torrent with hash {torrent_hash}")
        return True

    else:
        logging.info(f"Skipping label {label_name} creation in torrent with hash {torrent_hash}")
        return False


def rm_label(client: Client,
             torrent_hash: str,
             label_name: str
             ) -> bool:
    """
    Remove a label from a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param label_name: name of the label
    :return: True if the label is removed, False if it does not exist
    """

    exists = find_label(client, torrent_hash, label_name)

    if not exists:
        logging.info(f"Skipping label {label_name} deletion in torrent with hash {torrent_hash}")
        return False

    else:
        torrent_labels = client.get_torrent(torrent_hash).labels
        torrent_labels_new = []

        for label in torrent_labels:
            if label == label_name:
                pass
            else:
                torrent_labels_new.append(label)

        logging.info(f"Removed label {label_name} in torrent with hash {torrent_hash}")
        return True
