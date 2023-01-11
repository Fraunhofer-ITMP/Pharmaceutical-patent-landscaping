# -*- coding: utf-8 -*-

"""Script for creation of patent-enriched Alzheimer's knowledge graph."""

import logging
import pandas as pd
from pemt.chemical_extractor.experimental_data_extraction import extract_chemicals
from pemt.constants import PATENT_DIR
from pemt.patent_extractor.patent_chemical_harmonizer import harmonize_chemicals
from pemt.patent_extractor.patent_enrichment import extract_patent

from src.assignee_ontology import harmonize_names
from src.constants import PATENT_DIR, CHROMEDRIVER_PATH, BASE_FILES

logger = logging.getLogger(__name__)

"""
The base data was obtained using the PEMT tool using the example code. 
https://github.com/Fraunhofer-ITMP/PEMT/blob/main/example/example.py#L90
"""


def run_from_gene_pipeline():
    """Extracting patent data using PEMT tool."""

    genes = pd.read_csv(f'{BASE_FILES}/ad_proteins.csv', dtype=str)['symbol'].tolist()
    name = 'ad'  # Analysis name
    os = 'windows'

    extract_chemicals(
        analysis_name=name,
        gene_list=genes,
        is_uniprot=False,
    )

    harmonize_chemicals(analysis_name=name, from_genes=True)

    # patent_df = extract_patent(
    #     analysis_name=name,
    #     chrome_driver_path=CHROMEDRIVER_PATH,
    #     os_system=os,
    #     patent_year=2000,
    # )
    #
    # if patent_df.empty:
    #     logger.info(f"No patents found!")
    #     return None
    #
    # logger.info(f"Done with retrieval of patents")
    # logger.info(f"Data file can be found under {PATENT_DIR}")
    return


def data_normalization():
    harmonize_names(
        patent_df=pd.read_csv(f'{PATENT_DIR}/ad_patent_data.tsv', sep='\t'),
        analysis_name='ad'
    )


if __name__ == '__main__':
    run_from_gene_pipeline()


