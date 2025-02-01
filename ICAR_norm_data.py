#!/usr/bin/env python3
"""
Updated ICAR_norm_data.py: Processes norm data for ICAR tests using robust path handling,
error checking, and without extraneous debug calls.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

def process_icar_norm_data():
    code_directory = Path.cwd()
    # Find the parent folder of the current directory
    parent_directory = code_directory.parent
    project_path = parent_directory.parent
    codebook_directory = project_path / 'ICAR'

    ICAR16_norm_path = project_path / 'ICAR' / 'ICAR16' / 'ICAR 16 norm data'
    ICAR60_norm_path = project_path / 'ICAR' / 'ICAR60' / 'ICAR 60 norm data'

    ICAR16_norm_raw_data_path = 'sapaICARData18aug2010thru20may2013.csv'
    ICAR60_norm_raw_data_path = 'sapaData20may2013thru10jun2014.csv'

    # Check that the codebook exists
    codebook_file = codebook_directory / 'ICAR Item Key.xlsx'
    if not codebook_file.exists():
        raise FileNotFoundError(f"Codebook not found: {codebook_file}")
    codebook_all = pd.read_excel(codebook_file)
    
    # Process ICAR 16 norm data
    icar16_file = ICAR16_norm_path / ICAR16_norm_raw_data_path
    if not icar16_file.exists():
        raise FileNotFoundError(f"ICAR16 raw data file not found: {icar16_file}")
    ICAR_16_Norm_data = pd.read_csv(icar16_file, low_memory=False)
    
    for d in codebook_all.dimension.unique():
        # ICAR 16 calculation for each dimension
        dimension_column_names = codebook_all[codebook_all.dimension == d]['ICAR16'].unique()
        ICAR_16_Norm_data_slice = ICAR_16_Norm_data[ICAR_16_Norm_data.columns.intersection(dimension_column_names)]
        dimension_df = pd.DataFrame({d: ICAR_16_Norm_data_slice.sum(axis=1)}, index=ICAR_16_Norm_data_slice.index)
        # ICAR 60 calculation based on ICAR16 data
        dimension_column_names_60 = codebook_all[codebook_all.dimension == d]['ICAR60_original'].unique()
        ICAR_16_Norm_data_slice_60 = ICAR_16_Norm_data[ICAR_16_Norm_data.columns.intersection(dimension_column_names_60)]
        dimension_df_60 = pd.DataFrame({f'{d}_60': ICAR_16_Norm_data_slice_60.sum(axis=1) * (len(dimension_column_names_60) / 4)},
                                       index=ICAR_16_Norm_data_slice_60.index)
        ICAR_16_Norm_data = pd.concat([ICAR_16_Norm_data, dimension_df, dimension_df_60], axis=1)

    # Compute total scores for ICAR16 and adjusted ICAR60
    ICAR_16_Norm_data['ICAR16_Total'] = ICAR_16_Norm_data[codebook_all.dimension.unique()].sum(axis=1)
    ICAR_16_Norm_data['ICAR60_Total'] = ICAR_16_Norm_data[[f"{x}_60" for x in codebook_all.dimension.unique()]].sum(axis=1)

    # Process ICAR 60 norm data
    icar60_file = ICAR60_norm_path / ICAR60_norm_raw_data_path
    if not icar60_file.exists():
        raise FileNotFoundError(f"ICAR60 raw data file not found: {icar60_file}")
    ICAR_60_Norm_data = pd.read_csv(icar60_file, low_memory=False)
    columns_ICAR60 = list(codebook_all.ICAR60.unique())
    ICAR_60_Norm_data['ICAR16_Total'] = ICAR_60_Norm_data[ICAR_60_Norm_data.columns.intersection(columns_ICAR60)].sum(axis=1)
    
    for d in codebook_all.dimension.unique():
        dimension_column_names = codebook_all[codebook_all.dimension == d]['ICAR60'].unique()
        ICAR_60_Norm_data_slice = ICAR_60_Norm_data[ICAR_60_Norm_data.columns.intersection(dimension_column_names)]
        dimension_df = pd.DataFrame({d: ICAR_60_Norm_data_slice.sum(axis=1)}, index=ICAR_60_Norm_data_slice.index)
        dimension_df_60 = pd.DataFrame({f'{d}_60': ICAR_60_Norm_data_slice.sum(axis=1) * (len(dimension_column_names) / 4)},
                                       index=ICAR_60_Norm_data_slice.index)
        ICAR_60_Norm_data = pd.concat([ICAR_60_Norm_data, dimension_df, dimension_df_60], axis=1)

    ICAR_60_Norm_data['ICAR60_Total'] = ICAR_60_Norm_data[[f"{x}_60" for x in codebook_all.dimension.unique()]].sum(axis=1)
    
    norm_data_columns = ['age'] + ['ICAR16_Total'] + ['ICAR60_Total'] + list(codebook_all.dimension.unique()) + [f"{x}_60" for x in codebook_all.dimension.unique()]
    ICAR_Norm_data_use = ICAR_60_Norm_data[norm_data_columns]

    output_path = codebook_directory / 'ICAR_Norm_Data.csv'
    ICAR_Norm_data_use.to_csv(output_path, index=False)

if __name__ == '__main__':
    process_icar_norm_data()
