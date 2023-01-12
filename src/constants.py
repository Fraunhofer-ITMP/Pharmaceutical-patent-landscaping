# -*- coding: utf-8 -*-

"""File containing all constant required for the codebase."""

import os

"""Scraping related constant"""
CHROMEDRIVER_PATH = "C:/Users/Yojana.Gadiya/Downloads/chromedriver"

"""Neo4J related details"""

"""File paths."""
DATA_DIR = '../data'
BASE_FILES = os.path.join(DATA_DIR, 'raw')
PATENT_DIR = os.path.join(DATA_DIR, 'patent_dumps')
GRAPH_DIR = os.path.join(DATA_DIR, 'graph')
MAPPER_DIR = os.path.join(DATA_DIR, 'mapper')


