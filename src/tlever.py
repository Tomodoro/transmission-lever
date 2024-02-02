#!/usr/bin/env python

import os
import sys
import json
import logging
import argparse
from tlever_client import get_client, get_rpc_semver
from tlever_category import mk_category, rm_category, enforce_categories
from tlever_label import mk_label, rm_label
from tlever_tag import mk_tag, rm_tag
from tlever_tier import set_tiers, unset_tiers, activate_tiers

f = open(os.path.dirname(__file__) + "/../transmission-lever.json")

cfg = json.load(f)

client = get_client(cfg)

# create the top level parser
parser = argparse.ArgumentParser(
    description='simplifies common chores on torrents by wrapping the RPC',
    epilog='not all RPC methods are properly documented on upstream')

parser.add_argument('-v', '--verbose',
                    action='store_true')

subparsers = parser.add_subparsers(help='modifier on a torrent',
                                   dest='subparser_name',
                                   required=True)

# create the parser for the "category" command
subparser_category = subparsers.add_parser('category',
                                           help='manages categories of torrents')

subparser_category.add_argument('action',
                                type=str,
                                choices=['add', 'remove'],
                                help='action to perform')

subparser_category.add_argument('name',
                                type=str,
                                help='the name of the category')
subparser_category.add_argument('hash',
                                type=str,
                                help='the hash of the torrent')

# create the parser for the "label" command
subparser_label = subparsers.add_parser('label',
                                        help='manages labels of torrents')

subparser_label.add_argument('action',
                             type=str,
                             choices=['add', 'remove'],
                             help='action to perform')

subparser_label.add_argument('name',
                             type=str,
                             help='the name of the label')
subparser_label.add_argument('hash',
                             type=str,
                             help='the hash of the torrent')

# create the parser for the "tag" command
subparser_label = subparsers.add_parser('tag',
                                        help='manages tags of torrents')

subparser_label.add_argument('action',
                             type=str,
                             choices=['add', 'remove'],
                             help='action to perform')

subparser_label.add_argument('name',
                             type=str,
                             help='the name of the tag')
subparser_label.add_argument('hash',
                             type=str,
                             help='the hash of the torrent')

# create the parser for the "tier" command
subparser_label = subparsers.add_parser('tier',
                                        help='manages upload limit based on ratio')

subparser_label.add_argument('action',
                             type=str,
                             choices=['set', 'unset', 'activate'],
                             help='action to perform')

# create the parser for the "enforce" command
subparser_label = subparsers.add_parser('enforce',
                                        help='enforces a modifier on a torrent')

subparser_label.add_argument('action',
                             type=str,
                             choices=['category', 'tier'],
                             help='modifier to enforce')

# parse arguments
args = parser.parse_args()

# debug on
if args.verbose:
    logging.basicConfig(level=logging.INFO)
    print(vars(args))
else:
    logging.basicConfig(level=logging.WARNING)

if args.subparser_name == 'category':
    if args.action == 'add':
        mk_category(cfg, args.hash, args.name)

    elif args.action == 'remove':
        rm_category(cfg, args.hash, args.name)

elif args.subparser_name == 'label':
    if args.action == 'add':
        mk_label(client, args.hash, args.name)

    elif args.action == 'remove':
        rm_label(client, args.hash, args.name)

elif args.subparser_name == 'tag':
    if args.action == 'add':
        mk_tag(cfg, args.hash, args.name)

    elif args.action == 'remove':
        rm_tag(cfg, args.hash, args.name)

elif args.subparser_name == 'tier':
    if args.action == 'set':
        set_tiers(cfg)

    elif args.action == 'unset':
        unset_tiers(cfg)

    elif args.action == 'activate':
        activate_tiers(cfg)

elif args.subparser_name == 'enforce':
    if args.action == 'category':
        enforce_categories(cfg)

    elif args.action == 'tier':
        set_tiers(cfg)
        activate_tiers(cfg)
