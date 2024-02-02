#!/usr/bin/env pyhton

import os
import logging


def find_directory(directory: str) -> bool:

    """
    Find a directory in the filesystem
    :param directory: target directory
    :return: True if directory is found, False otherwise
    """

    exists = os.path.exists(directory)

    if not exists:
        logging.info(f"No directory {directory} in filesystem")
        return False

    logging.info(f"Found directory {directory} in filesystem")
    return True


def empty_directory(directory: str) -> bool:

    """
    Check if directory is empty
    :param directory: target directory
    :return: True if directory is empty, False otherwise
    """

    children = os.listdir(directory)

    if len(children) == 0:
        logging.info(f"Directory {directory} is empty")
        return True

    logging.info(f"Directory {directory} is not empty")
    return False


def relative_directory(full_path, base_path) -> str:

    """
    Get relative directory
    :param full_path: the full path directory
    :param base_path: the base path directory
    :return: relative directory, if dot return empty string
    """

    rel_path = os.path.relpath(full_path, base_path)

    if rel_path == '.':
        return ''
    else:
        return str(rel_path)


def mk_directory(directory: str) -> bool:

    """
    Create a directory in the filesystem
    :param directory: directory to create
    :return: True if directory is created, False if it already exists
    """

    exists = find_directory(directory)

    if not exists:
        os.makedirs(directory)
        logging.info(f"Created directory {directory}")
        return True

    logging.info(f"Skipping directory creation: directory {directory} already exists")
    return False


def rm_directory(directory: str) -> bool:

    """
    Remove a directory in the filesystem
    :param directory: directory to delete
    :return: True if directory is deleted, False otherwise
    """

    exists = find_directory(directory)

    if not exists:
        logging.info(f"Skipping directory deletion: directory {directory} does not exist")
        return False

    empty = empty_directory(directory)

    if not empty:
        logging.info(f"Skipping directory deletion: directory {directory} is not empty")
        return False

    os.rmdir(directory)
    logging.info(f"Deleted directory {directory}")
    return True
