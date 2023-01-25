# -*- coding: utf-8 -*-

"""Script for generation of patent corpora for rare diseases."""

import logging
import os
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

from src.constants import GRAPH_DIR, BASE_FILES, PATENT_DIR
from src.util import enrich_patent, annotate_genes, chemical_to_smiles, get_chemical_max_phase

logger = logging.getLogger(__name__)

os.makedirs(GRAPH_DIR, exist_ok=True)


def load_orphanet_df():
    """Create TSV file from Orphanet's XML data."""

    if os.path.exists(f'{BASE_FILES}/orphanet_2021.tsv'):
        df = pd.read_csv(f'{BASE_FILES}/orphanet_2021.tsv', sep='\t')
        return df

    df = pd.DataFrame(columns=[
        'db_id',
        'disease_name',
        'gene_symbol',
        'pmid'
    ])

    tree = ET.parse(f'{BASE_FILES}/en_product6.xml')
    root = tree.getroot()

    for disease_data in tqdm(root.find('DisorderList'), desc='Reading XML file'):
        df_data = {}
        for data in disease_data:
            if data.tag == 'OrphaCode':
                df_data['db_id'] = data.text
            elif data.tag == 'Name':
                df_data['disease_name'] = data.text
            elif data.tag == 'DisorderGeneAssociationList':
                for rel_data in data:
                    for rel in rel_data:
                        if rel.tag == 'SourceOfValidation':
                            df_data['pmid'] = rel.text
                        elif rel.tag == 'Gene':
                            df_data['gene_symbol'] = rel.find('Symbol').text

                    tmp_df = pd.DataFrame(df_data, index=[0])
                    df = pd.concat([df, tmp_df], ignore_index=True)

    df.to_csv(f'{BASE_FILES}/orphanet_2021.tsv', sep='\t', index=False)

    return df


if __name__ == '__main__':
    orphanet_df = load_orphanet_df()
    genes = orphanet_df['gene_symbol'].tolist()
    name = 'orphanet'  # Analysis name
    os = 'windows'

    enrich_patent(
        name=name,
        gene_list=genes,
        os_name=os,
    )

    # Get chemical mapping file
    patent_df = pd.read_csv(f'{PATENT_DIR}/orphanet_normalized_patent_data.tsv', sep='\t')
    chemical_to_smiles(
        chemical_patent_df=patent_df,
        analysis_name=name
    )

    # Chemical phase annotations
    get_chemical_max_phase(
        chemical_patent_df=patent_df,
        analysis_name=name
    )
