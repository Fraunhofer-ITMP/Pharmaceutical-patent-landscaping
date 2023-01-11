# -*- coding: utf-8 -*-

"""Script for normalizing the assignee information from patent documents."""

from typing import List, Dict
import pandas as pd


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
