# -*- coding: utf-8 -*-

"""Code with base functions to be used for the creation of graphs."""

import chembl_downloader
import json
import logging
import pandas as pd
from chembl_webresource_client.new_client import new_client
from collections import defaultdict
from pemt.chemical_extractor.experimental_data_extraction import extract_chemicals
from pemt.patent_extractor.patent_chemical_harmonizer import harmonize_chemicals
from pemt.patent_extractor.patent_enrichment import extract_patent
from tqdm import tqdm
from typing import List

from src.constants import CHROMEDRIVER_PATH, PATENT_DIR, MAPPER_DIR
from src.normalizer import harmonize_names

logger = logging.getLogger('__name__')

"""
The base data was obtained using the PEMT tool using the example code. 
https://github.com/Fraunhofer-ITMP/PEMT/blob/main/example/example.py#L90
"""


def enrich_patent(
    gene_list: List[str],
    name: str,
    os_name: str = 'windows',
) -> None:
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


def annotate_genes(
    chemical_patent_df: pd.DataFrame,
    analysis_name: str,
) -> None:
    """Annotation of genes within the patent data.

    @:param chemical_patent_df: Dataframe with patent data annotated using PEMT.
    @:param analysis_name: Name of the analysis
    """

    # Genes chemical data
    gene_dict = json.load(open(f"{MAPPER_DIR}/{analysis_name}_gene_to_chemicals.json"))

    chemical_dict = defaultdict(set)

    for gene, chemical_ids in tqdm(
        gene_dict.items(), desc="Creating the chemical-gene dictionary"
    ):
        for chemical in chemical_ids:
            chemical_dict[chemical].add(gene)

    chemical_patent_df["genes"] = chemical_patent_df["chembl"].map(
        lambda x: ", ".join(chemical_dict.get(x, []))
    )

    chemical_patent_df.to_csv(
        f"{PATENT_DIR}/{analysis_name}_gene_enumerated_patent_data.tsv", sep="\t", index=False
    )


def chemical_to_smiles(
    chemical_patent_df: pd.DataFrame,
    analysis_name: str,
):
    """Create mapper file for ChEMBL id to SMILES.

    @:param chemical_patent_df: Dataframe with patent data annotated using PEMT.
    @:param analysis_name: Name of the analysis
    """

    chemicals = set(chemical_patent_df['chembl'].unique())

    smiles_dict = defaultdict(str)

    molecule_server = new_client.molecule

    for chembl_idx in tqdm(chemicals):
        comp_struct = molecule_server.filter(chembl_id=chembl_idx).only(['molecule_structures'])[0]
        smiles_dict[chembl_idx] = comp_struct['molecule_structures']['canonical_smiles']

    with open(f'{MAPPER_DIR}/{analysis_name}_chem_smile_mapper.json', 'w') as f:
        json.dump(smiles_dict, f, ensure_ascii=False, indent=2)


def get_chemical_max_phase(
    chemical_patent_df: pd.DataFrame,
    analysis_name: str,
):
    """Create mapper file for ChEMBL id to SMILES.

    @:param chemical_patent_df: Dataframe with patent data annotated using PEMT.
    @:param analysis_name: Name of the analysis
    """

    chemicals = set(chemical_patent_df['chembl'].unique())

    sql = """\
    SELECT 
        MOLECULE_DICTIONARY.CHEMBL_ID as chembl_id,
        DRUG_INDICATION.MAX_PHASE_FOR_IND as max_phase
    FROM MOLECULE_DICTIONARY
    JOIN DRUG_INDICATION ON MOLECULE_DICTIONARY.MOLREGNO == DRUG_INDICATION.MOLREGNO"""

    _, version = chembl_downloader.download_extract_sqlite(return_version=True)
    logger.warning(f'Working on ChEMBL version {version}')

    phase_data = chembl_downloader.query(sql=sql)
    phase_data = phase_data[phase_data['chembl_id'].isin(chemicals)]
    phase_data = phase_data.sort_values('max_phase', ascending=False).drop_duplicates('chembl_id').sort_index()

    phase_data.to_csv(f'{MAPPER_DIR}/{analysis_name}_chemical_max_phase.tsv', sep='\t', index=False)
