# -*- coding: utf-8 -*-

"""Script for creation of Patent-enriched rare disease BEL knowledge graph."""

import logging
import os
import xml.etree.ElementTree as ET

import pandas as pd
from tqdm import tqdm
from pemt.chemical_extractor.experimental_data_extraction import extract_chemicals
from pemt.constants import PATENT_DIR
from pemt.patent_extractor.patent_chemical_harmonizer import harmonize_chemicals
from pemt.patent_extractor.patent_enrichment import extract_patent

from src.assignee_ontology import harmonize_names
from src.constants import PATENT_DIR, GRAPH_DIR, BASE_FILES, CHROMEDRIVER_PATH

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


def run_from_gene_pipeline():
    """Extracting patent data using PEMT tool."""

    orphanet_df = load_orphanet_df()
    genes = orphanet_df['gene_symbol'].tolist()
    name = 'orphanet'  # Analysis name
    os = 'windows'

    extract_chemicals(
        analysis_name=name,
        gene_list=genes,
        is_uniprot=False,
    )

    harmonize_chemicals(analysis_name=name, from_genes=True)

    patent_df = extract_patent(
        analysis_name=name,
        chrome_driver_path=CHROMEDRIVER_PATH,
        os_system=os,
        patent_year=2000,
    )

    if patent_df.empty:
        logger.info(f"No patents found!")
        return None

    logger.info(f"Done with retrieval of patents")
    logger.info(f"Data file can be found under {PATENT_DIR}")
    return


def data_normalization():
    harmonize_names(
        patent_df=pd.read_csv(f'{PATENT_DIR}/ad_patent_data.tsv', sep='\t'),
        analysis_name='ad'
    )




if __name__ == '__main__':
    create_graph()
