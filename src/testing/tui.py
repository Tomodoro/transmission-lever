#!/usr/bin/env python

import curses
import traceback

from core.client import get_client, get_torrents_list
from core.torrent import get_stub_info


def get_config_prefixes(config: dict) -> dict:
    """
    Returns a dictionary with label prefixes
    :param config: valid configuration dictionary
    :return: dictionary with prefixes
    """

    prefixes = {
        "category": config['General']['prefix']['categories'],
        "tier": config['General']['prefix']['tiers'],
        "tag": config['General']['prefix']['tags']
    }

    return prefixes


def prettify_stub_info(config,
                       torrent_hash
                       ) -> dict:
    """
    Pretty format info of a torrent
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :return: a prettified formatted dictionary
    """

    client = get_client(config)
    prefixes = get_config_prefixes(config)
    info = get_stub_info(client, torrent_hash, prefixes)

    output = {
        'Name': info.name,
        'Hash': info.hash,
        'Ratio': info.ratio_pretty,
        'Progress': info.progress,
        'Status': info.status,
        'Group': info.group,
        'Tier': info.tier,
        'Category': info.category,
        'Tag': info.tag,
        'Up Speed': info.up_pretty,
        'Down Speed': info.down_pretty,
        'ETA': info.eta
    }

    return output


def curses_single(config, torrent_hash):
    """
    Wrapper for Terminal Interface for ncurses
    :return: None
    """

    def ncurses_app(stdscr) -> None:

        """
        Terminal Interface for ncurses
        :return: None
        """

        try:
            # init curses
            ch = ''
            stdscr = curses.initscr()
            curses.cbreak()
            stdscr.timeout(2000)

            # while non-quit char
            while ch != ord('q'):

                info = prettify_stub_info(config, torrent_hash=torrent_hash)

                i = 0
                p = '     '
                for k, v in info.items():
                    stdscr.addstr(1 + i, 1, f"  {k}: {v}{p}", curses.A_NORMAL)
                    i += 1

                stdscr.clrtoeol()
                stdscr.refresh()
                ch = stdscr.getch()

        except:
            traceback.print_exc()
        finally:
            curses.endwin()

    curses.wrapper(ncurses_app)

def curses_tier(config: dict) -> None:
    """
    Wrapper function for terminal interface for curses
    :param config: valid configuration dictionary
    :param torrent_hash: a single torrent hash
    :return: None
    """

    client = get_client(config)
    prefixes = get_config_prefixes(config)

    def ncurses_app(stdscr) -> None:

        """
        Terminal Interface for ncurses
        :return: None
        """

        try:
            # init curses
            ch = ''
            stdscr = curses.initscr()
            curses.cbreak()
            stdscr.timeout(2000)

            # while non-quit char
            while ch != ord('q'):

                torrents_list = get_torrents_list(client)

                t_a = "{:<30}".format("Torrent Name")
                t_b = "{:<10}".format("Up Speed")
                t_c = "{:<10}".format("Up Limit")
                t_d = "{:<10}".format("Down Speed")
                t_e = "{:<10}".format("Down Limit")
                t_f = "{:<7}".format("Ratio")
                t_g = "{:<7}".format("Limit")

                stdscr.addstr(1, 1, f"{t_a}  {t_b}  {t_c}  {t_d}  {t_e}  {t_f}  {t_g}", curses.A_BOLD)

                i = 1
                for torrent in torrents_list:
                    info = get_stub_info(client, torrent.hashString, prefixes)
                    a = "{:<30}".format(info.name[:30])
                    b = "{:<10}".format(info.up_pretty.split('- ')[0])
                    if len(info.up_pretty.split('-')) == 1:
                        c = "{:<10}".format('Off')
                    else:
                        c = info.up_pretty.split('-')[1]
                        c = c.replace('[', '')
                        c = c.replace(']', '')
                        c = "{:<10}".format(c[1:])
                    d = "{:<10}".format(info.down_pretty.split('-')[0])
                    if len(info.down_pretty.split('-')) == 1:
                        e = "{:<10}".format('Off')
                    else:
                        e = info.down_pretty.split('-')[1]
                        e = e.replace('[', '')
                        e = e.replace(']', '')
                        e = "{:<10}".format(e[1:])
                    f = "{:<7}".format(info.ratio)
                    g = "{:<7}".format(info.ratio_limit)
                    stdscr.addstr(1 + i, 1, f"{a}  {b}  {c}  {d}  {e}  {f}  {g} ", curses.A_NORMAL)
                    i += 1

                stdscr.clrtoeol()
                stdscr.refresh()
                ch = stdscr.getch()

        except:
            traceback.print_exc()
        finally:
            curses.endwin()

    curses.wrapper(ncurses_app)
