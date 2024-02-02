# /usr/bin/env python

from tlever_label import find_label, find_regex_label, sw_label, rm_label
from tlever_client import get_client, get_torrents_list


def upd_tier(num: str,
             config: dict,
             torrent_hash: str) -> None:
    client = get_client(config)
    prefix_char = config['General']['prefix']['tiers']
    new_label = prefix_char + "tier-" + num
    old_label = prefix_char + "tier-" + str(int(num) - 1)

    sw_label(client, torrent_hash, old_label, new_label)
    client.change_torrent(ids=[torrent_hash],
                          seed_idle_mode=config["Tiers"][num]["seed_idle_mode"],
                          seed_ratio_mode=config["Tiers"][num]["seed_ratio_mode"],
                          upload_limit=config["Tiers"][num]["upload_limit"],
                          upload_limited=config["Tiers"][num]["upload_limited"])


def set_tiers(config: dict) -> None:
    """
    Set bandwidth limits through tier labels
    :param config: valid configuration dictionary
    :return: None
    """

    client = get_client(config)

    for torrent in get_torrents_list(client):
        ratio = torrent.ratio
        torrent_hash = torrent.hashString
        free = find_label(client, torrent_hash, "tier free")
        progress = torrent.progress

        # Check if torrent is complete
        if progress != 100:
            continue

        # Maintain Tier free
        elif free:
            client.change_torrent(ids=[torrent_hash],
                                  upload_limited=False,
                                  seed_ratio_mode=2,
                                  seed_idle_mode=2)

        # Set Tier 0
        elif ((ratio >= 0)
              and (ratio < config["Tiers"]["0"]["seed_ratio_limit"])):
            upd_tier("0", config, torrent_hash)

        # Set Tier 1-9
        else:
            for i in range(1, 10):
                new_num = str(i)
                old_num = str(i - 1)
                if ((ratio >= config["Tiers"][old_num]["seed_ratio_limit"])
                        and (ratio < config["Tiers"][new_num]["seed_ratio_limit"])):
                    upd_tier(new_num, config, torrent_hash)
                    break

            else:
                print(f"Ratio {ratio} out of bounds for torrent with hash {torrent_hash}")


def unset_tiers(config: dict) -> None:

    """
    Remove tier labels and reset upload limits
    :param config: valid configuration dictionary
    :return: None
    """

    client = get_client(config)
    prefix_char = config['General']['prefix']['tiers']

    for torrent in get_torrents_list(client):
        torrent_hash = torrent.hashString

        for i in range(0,10):
            tier_label = prefix_char + "tier-" + str(i)
            exists = find_regex_label(client, torrent_hash, tier_label)

            if exists:
                rm_label(client, torrent_hash, tier_label)
                break
