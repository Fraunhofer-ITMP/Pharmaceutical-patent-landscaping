# -*- coding: utf-8 -*-

"""Script for normalizing the assignee information from patent documents."""

import pandas as pd
from typing import Dict

from src.constants import PATENT_DIR, MAPPER_DIR


def get_all_assignee(
    patent_data: pd.DataFrame,
    output_file_path: str,
) -> None:
    """Method to get all unique assignee from the patent data.

    @param patent_data: Dataframe containing patent data
    @param output_file_path: The path where to store the output file
    """
    organization = set(patent_data['assignee'].tolist())

    df = pd.DataFrame(
        organization,
        columns=['Organization name']
    )
    df.sort_values(by='Organization name', inplace=True)

    df.to_csv(output_file_path, sep='\t', index=False)


def normalize_assignee(
    patent_data: pd.DataFrame,
    mapping_col_data: Dict[str, Dict[str, str]],
    output_file_path: str,
) -> None:
    """Mapping the custom annotations to the resultant patent data.

    @param patent_data: Dataframe containing patent data
    @param mapping_col_data: A list of dictionaries with the key as the new column name and value as a dictionary
    containing the mapping between the initial assignee name with the custom assignee name.
    @param output_file_path: The path where to store the output file
    """
    for new_column_name, mapping_dict in mapping_col_data.items():
        patent_data[new_column_name] = patent_data['assignee'].map(lambda x: mapping_dict.get(x))

    patent_data.to_csv(output_file_path, sep='\t', index=False)


def harmonize_names(
    patent_df: pd.DataFrame,
    analysis_name: str
):
    """Method to normalize the assignee names across the patent cohort."""

    patent_df['assignee'] = patent_df['assignee'].str.strip()  # remove leading white spaces
    patent_df['assignee'] = patent_df['assignee'].str.replace(
        'é', 'e').replace('É', 'E').replace('é', 'e').replace('—', '-').replace('ò', 'o').replace('Ö', 'O').replace(
        'ä', 'a').replace('Ä', 'A').replace('ü', 'u').replace('Ü', 'U').replace('Ó', 'O').replace('ó', 'o').replace(
        'È', 'E').replace('A′', 'A').replace('À', 'A').replace('Í', 'I').replace('Ç', 'C').replace('Å', 'A').replace(
        'á', 'a').replace('Á', 'A').replace('Ã', 'A').replace('Ø', 'O').replace('Ł', 'L')

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
