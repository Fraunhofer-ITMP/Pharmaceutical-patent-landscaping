# -*- coding: utf-8 -*-

"""Script for generation of patent corpora for neurodegenerative diseases."""

import pandas as pd

from src.constants import BASE_FILES, PATENT_DIR
from src.util import enrich_patent, annotate_genes, chemical_to_smiles, get_chemical_max_phase

if __name__ == '__main__':
    genes = pd.read_csv(f'{BASE_FILES}/ad_proteins.csv', dtype=str)['symbol'].tolist()
    name = 'ad'  # Analysis name
    os = 'windows'

    enrich_patent(
        name=name,
        gene_list=genes,
        os_name=os
    )

    # Get chemical mapping file
    patent_df = pd.read_csv(f'{PATENT_DIR}/ad_normalized_patent_data.tsv', sep='\t')
    chemical_to_smiles(
        chemical_patent_df=patent_df,
        analysis_name=name
    )

    # Get phase annotation for compounds
    get_chemical_max_phase(
        chemical_patent_df=patent_df,
        analysis_name=name
    )
