# Transmission Lever

Small program that simplifies common chores on torrents by wrapping the RPC.
This program is not meant to be a manager by itself, only a *lever*
for others to write their own automatized tools.

## Installation

This python is written in python.

1. Clone the repo:
```bash
git clone https://github.com/Tomodoro/transmission-lever.git tlever
```

2. Enter the repo:
```bash
cd tlever
```

3. Create an environment
```bash
python -m venv .env
```

4. Activate the environment
```bash
. .env/bin/activate
```

5. Install `transmission-rpc`:
```bash
pip3 install transmission-rpc
```

6. Copy configuration file from example:
```bash
cp transmission-lever.json.example transmission-lever.json
```

7. Check help:
```bash
python src/tlever.py --help
```

## CLI Usage

### Categories

To organize torrents in folders the same way as clients like qBittorrent,
a label-based system marks the torrents and moves them to the location.

All paths are relative to the `Downloads` directory, this is read from
the transmission configuration file.

For example, to move `<torrent-hash>` into the *movies* category.
```bash
python src/tlever.py category add movies <torrent-hash>
```

This will add the label `@movies` to the torrent and move its data to:
```
Downloads/
└── movies
    └── torrent-name
```

To undo the action:
```bash
python src/tlever.py category remove movies <torrent-hash>
```

This will remove the label `@movies` to the torrent and movie its data to:
```
Downloads/
└── torrent-name
```

> This command does not clean up empty directories,
> this is because the program is using the RPC to move torrent data
> and it does not have permissions over the filesystem in all use cases.
> 
> Hooking the command `find /path/to/Downloads -type d -empty -delete` to a script
> triggered by added|done|done_seeding of a torrent does the trick.

If labels get desync from the torrent directory, you can enforce the category label directory:
```bash
python src/tlever.py enforce category
```

### Tags

To separate common labels from category labels,
a tag with a prefix is used.

For example, to tag `<torrent-hash>` with *best-of-the-year*:
```bash
python src/tlever.py tag add best-of-the-year <torrent-hash>
```

This will add the label `#best-of-the-year` to the torrent.

To undo the action:
```bash
python src/tlever.py tag remove best-of-the-year <torrent-hash>
```

This will remove the label `#best-of-the-year` to the torrent.

> This command *is not* equivalent to `tier.py label ...`
> as it is *always* prefixed.

### Tiers

To set upload speed throttling based on ratio,
this is based on [qbitseedmgr](https://github.com/Tomodoro/qbitseedmgr).

To start managing torrents:
```bash
python src/tlever.py tier set
```

To stop managing torrents:
```bash
python src/tlever.py tier unset
```

To resume paused torrents:
```bash
python src/tlever.py tier activate
```

> It seems that the RPC does not expose the number of seeds,
> so it's not possible to port `not-popular`.

To keep the tiers updated and active:
```bash
python src/tlever.py enforce tier

```

### Labels

To manage labels without prefixes, useful to fix torrents that have
 invalid categories or tags because of a change on their prefix.

For example, given the prefixes `@` and `#` for categories and tags respectively,
it's desired to remove the invalid tag `%monthly-release`
from `<torrent-hash>`:
```bash
python src/tlever.py label remove %monthly-release <torrent-hash>
```

To add an arbitrary label:
```bash
python src/tlever.py label add custom-label <torrent-hash>
```

## Module Usage

The files are split into high-level functions and low functions.

* Low-level functions interact directly with the RPC or the shell.
* High-level functions do not interact directly with the RPC nor the shell.

The goal is to have a friendly wrapper with proper docstrings.

### High-level

* `tlever_category.py`: all actions related to a category.
* `tlever_tag.py`: all actions related to a tag.
* `tlever_tier.py`: all actions related to tiers

### Low-level

* `tlever_auth`: all RPC related to the current session.
* `tlever_label.py`: all RPC related to the labels.
* `tlever_torrent.py`: all RPC related to the torrents.
* `tlever_directory.py`: all shell calls related to the filesystem.
