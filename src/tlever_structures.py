#!/usr/bin/env python

class TorrentStub:

    """
    This class represents a subset of information about a torrent
    """

    def __init__(self,
                 name: str,
                 hash: str,
                 ratio: float,
                 ratio_limit: float,
                 ratio_limit_mode: int,
                 ratio_pretty: str,
                 progress: float,
                 group: str,
                 tier: int,
                 category: str,
                 tag: str,
                 eta: str,
                 up_speed_bytes: int,
                 up_limit_bytes: int,
                 up_limit_state: bool,
                 up_pretty: str,
                 down_speed_bytes: int,
                 down_limit_bytes: int,
                 down_limit_state: bool,
                 down_pretty: str):

        self.name = name
        self.hash = hash
        self.ratio = ratio
        self.ratio_limit = ratio_limit
        self.ratio_limit_mode = ratio_limit_mode
        self.ratio_pretty = ratio_pretty
        self.progress = progress
        self.group = group
        self.tier = tier
        self.category = category
        self.tag = tag
        self.eta = eta
        self.up_speed_bytes = up_speed_bytes
        self.up_limit_bytes = up_limit_bytes
        self.up_limit_state = up_limit_state
        self.up_pretty = up_pretty
        self.down_speed_bytes = down_speed_bytes
        self.down_limit_bytes = down_limit_bytes
        self.down_limit_state = down_limit_state
        self.down_pretty = down_pretty
