# -*- coding: utf-8 -*-

"""Script for normalizing the assignee information from patent documents."""

import os
import pandas as pd

from src.constants import PATENT_DIR, MAPPER_DIR
from src.normalizer import get_all_assignee, normalize_assignee


def harmonize_names(
    patent_df: pd.DataFrame,
    analysis_name: str
):
    """Method to normalize the assignee names across the patent cohort."""

    patent_df['assignee'] = patent_df['assignee'].str.strip()  # remove leading white spaces

    organization_mapper = pd.read_csv(
        f'{MAPPER_DIR}/assignee/organization.tsv', sep='\t', index_col='name', dtype=str, encoding='ISO-8859-1'
    ).to_dict()['harmonized_name']

    acquired_mapper = pd.read_csv(
        f'{MAPPER_DIR}/assignee/acquired.tsv', sep='\t', index_col='name', dtype=str,
    ).to_dict()['harmonized_name']

    individuals = pd.read_csv(
        f'{MAPPER_DIR}/assignee/individual.tsv', sep='\t', dtype=str,
    )['name'].to_list()

    normalize_assignee(
        patent_data=patent_df,
        mapping_col_data={
            'organization_name': organization_mapper,
            'acquired_by': acquired_mapper,
            'person': {person: True for person in individuals}
        },
        output_file_path=f'{PATENT_DIR}/{analysis_name}_normalized_patent_data.tsv'
    )
