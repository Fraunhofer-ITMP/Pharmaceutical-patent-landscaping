# -*- coding: utf-8 -*-

"""Script for creation of patent-enriched Alzheimer's knowledge graph."""

import pandas as pd

from src.constants import BASE_FILES
from src.util import enrich_patent

if __name__ == '__main__':
    genes = pd.read_csv(f'{BASE_FILES}/ad_proteins.csv', dtype=str)['symbol'].tolist()
    name = 'ad'  # Analysis name
    os = 'windows'

    enrich_patent(
        name=name,
        gene_list=genes,
        os_name=os
    )
