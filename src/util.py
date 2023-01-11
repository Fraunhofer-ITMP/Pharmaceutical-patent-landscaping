# -*- coding: utf-8 -*-

"""Code with base functions to be used for the creation of graphs."""

import logging
from typing import List

from pemt.chemical_extractor.experimental_data_extraction import extract_chemicals
from pemt.patent_extractor.patent_chemical_harmonizer import harmonize_chemicals
from pemt.patent_extractor.patent_enrichment import extract_patent

from src.normalizer import harmonize_names
from src.constants import CHROMEDRIVER_PATH, PATENT_DIR

logger = logging.getLogger('__name__')

"""
The base data was obtained using the PEMT tool using the example code. 
https://github.com/Fraunhofer-ITMP/PEMT/blob/main/example/example.py#L90
"""


def enrich_patent(
    gene_list: List[str],
    name: str,
    os_name: str = 'windows',
):
    """Extracting patent data using PEMT tool."""

    extract_chemicals(
        analysis_name=name,
        gene_list=gene_list,
        is_uniprot=False,  # Both our cases use HGNC symbols
    )

    harmonize_chemicals(analysis_name=name, from_genes=True)

    patent_df = extract_patent(
        analysis_name=name,
        chrome_driver_path=CHROMEDRIVER_PATH,
        os_system=os_name,
        patent_year=2000,
    )

    if patent_df.empty:
        logger.info(f"No patents found!")
        return None

    # Normalizing the patent assignee names
    harmonize_names(
        patent_df=patent_df,
        analysis_name=name
    )

    logger.info(f"Done with retrieval of patents")
    logger.info(f"Data file can be found under {PATENT_DIR}")
    return


