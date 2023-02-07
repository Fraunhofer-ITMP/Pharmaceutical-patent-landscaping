# -*- coding: utf-8 -*-

"""Script for extracting the publication information from MovingTargets repository.

MovingTargets repository - https://github.com/BZdrazil/Moving_Targets
"""

import os

import pandas as pd
from tqdm import tqdm


def combine_publications():
    """Method to combine the different target class files."""
    combined_df = pd.DataFrame()

    for file_name in tqdm(os.listdir('../data/raw')):
        if not file_name.endswith('.gz'):
            continue

        df = pd.read_csv(
            file_name, compression='gzip',
            usecols=[
                'target_chembl_id',
                'publication_year',
                'PMID_count'
            ]
        )
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df.drop_duplicates(subset=['target_chembl_id', 'publication_year'], inplace=True)
    combined_df = combined_df[combined_df['publication_year'] < 2000]
    combined_df.to_csv('target_publication_year.tsv.gz', index=False, sep='\t', compression='gzip')


def map_chembl_targets():
    """Mapping the ChEMBL protein ids to HGNC target names."""

    chembl_mapper = pd.read_csv(
        'https://raw.githubusercontent.com/Fraunhofer-ITMP/PEMT/main/data/mapper/chembl_uniprot_mapping.txt',
        sep='\t',
        skiprows=1,
        names=['uniprot', 'chembl_id', 'target_name', 'target_type']
    )
    chembl_mapper.set_index('chembl_id', inplace=True)
    chembl_mapper = chembl_mapper[['uniprot']]
    chembl_mapper = chembl_mapper.to_dict()['uniprot']

    publication_df = pd.read_csv(
        'target_publication_year.tsv.gz', sep='\t', compression='gzip'
    )
    publication_df['uniprot'] = publication_df['target_chembl_id'].map(chembl_mapper)

    uniprot_to_hgnc = pd.read_csv(
        'https://raw.githubusercontent.com/Fraunhofer-ITMP/PEMT/main/data/mapper/hgnc_mapper.tsv',
        sep='\t',
        usecols=['Approved symbol', 'UniProt ID(supplied by UniProt)'],
        index_col='UniProt ID(supplied by UniProt)'
    ).to_dict()['Approved symbol']

    publication_df['hgnc'] = publication_df['uniprot'].map(uniprot_to_hgnc)

    publication_df.to_csv('target_publication_year.tsv.gz', sep='\t', compression='gzip', index=False)
