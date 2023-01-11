# -*- coding: utf-8 -*-

"""File containing all constant required for the codebase."""

import os

"""Scraping related constant"""
CHROMEDRIVER_PATH = "C:/Users/Yojana.Gadiya/Downloads/chromedriver"

"""Neo4J related details"""

"""File paths."""
HERE = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(HERE, '../data')
BASE_FILES = os.path.join(DATA_DIR, 'raw')
PATENT_DIR = os.path.join(DATA_DIR, 'patent_dumps')
GRAPH_DIR = os.path.join(DATA_DIR, 'graph')
MAPPER_DIR = os.path.join(DATA_DIR, 'mapper')
PLOT_DIR = os.path.join(DATA_DIR, 'plots')


