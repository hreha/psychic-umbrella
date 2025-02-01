import pandas as pd
import numpy as np
import os
from pathlib import Path
from scipy import stats

code_directory = os.getcwd() 
path_current = Path(code_directory)
# Find the parent folder of the code directory to be able to read data files
parent_directory = Path(path_current.parent.absolute())
project_path = Path(parent_directory.parent.absolute())
codebook_directory = os.path.join(project_path, 'ICAR')

ICAR16_norm_path = 'ICAR/ICAR16/ICAR 16 norm data/'
ICAR60_norm_path = 'ICAR/ICAR60/ICAR 60 norm data/'

ICAR16_norm_raw_data_path = 'sapaICARData18aug2010thru20may2013.csv'
ICAR60_norm_raw_data_path = 'sapaData20may2013thru10jun2014.csv'

codebook_all = pd.read_excel(os.path.join(codebook_directory, 'ICAR Item Key.xlsx'))
codebook_all.columns

# ICAR 16 calculation ###########
ICAR_16_Norm_data = pd.read_csv(os.path.join(project_path, ICAR16_norm_path, ICAR16_norm_raw_data_path),
                                low_memory=False)
ICAR_16_Norm_data['ICAR16_Total'].describe()
ICAR_16_Norm_data.columns
ICAR_16_Norm_data.age.describe()
#ICAR_16_Norm_data.gender.describe()
round(stats.percentileofscore(ICAR_16_Norm_data['ICAR16_Total'], 10, kind = 'strict').item(), 2)
for d in codebook_all.dimension.unique():
        # ICAR 16 calculation
        dimension_column_names = codebook_all[codebook_all.dimension == d]['ICAR16'].unique()
        ICAR_16_Norm_data_slice = ICAR_16_Norm_data[ICAR_16_Norm_data.columns.intersection(dimension_column_names)]
        dimension_df = pd.DataFrame({d: ICAR_16_Norm_data_slice.sum(axis=1)}, 
                                    index = list(ICAR_16_Norm_data_slice.index))
        # ICAR 60 calculation
        dimension_column_names_60 = codebook_all[codebook_all.dimension == d]['ICAR60_original'].unique()
        ICAR_16_Norm_data_slice_60 = ICAR_16_Norm_data[ICAR_16_Norm_data.columns.intersection(dimension_column_names_60)]
        dimension_df_60 = pd.DataFrame({f'{d}_60': ICAR_16_Norm_data_slice_60.sum(axis=1) * (len(dimension_column_names_60)/4)}, 
                                    index = list(ICAR_16_Norm_data_slice_60.index))
        
        ICAR_16_Norm_data = pd.concat([ICAR_16_Norm_data, dimension_df, dimension_df_60], axis = 1)

ICAR_16_Norm_data.columns.intersection(codebook_all[codebook_all.dimension == 'Matrix Reasoning']['ICAR60_original'].unique())
ICAR_16_Norm_data.columns.intersection(codebook_all.dimension.unique())
ICAR_16_Norm_data['Letter & Number_60'].describe()
ICAR_16_Norm_data['Verbal Reasoning_60'].describe()
ICAR_16_Norm_data['Matrix Reasoning_60'].describe()
ICAR_16_Norm_data['3D Rotation_60'].describe()
ICAR_16_Norm_data['ICAR16_Total'] = ICAR_16_Norm_data[codebook_all.dimension.unique()].sum(axis = 1)
ICAR_16_Norm_data['ICAR60_Total'] = ICAR_16_Norm_data[[x + "_60" for x in codebook_all.dimension.unique()]].sum(axis = 1)
ICAR_16_Norm_data['ICAR16_Total'].describe()

# For some reason the responses are not randomly and equally divided across dimensions. 
# For instance, VR and LN have more responses than MX and 3DR, making the _60 scores excessively large.
# Have to use the ICAR 60 norm data instead.

# ICAR 60 calculation ###############
ICAR_60_Norm_data = pd.read_csv(os.path.join(project_path, ICAR60_norm_path, ICAR60_norm_raw_data_path),
                                low_memory=False)
ICAR_60_Norm_data['ICAR16_Total'] = ICAR_60_Norm_data[ICAR_60_Norm_data.columns.intersection(codebook_all.ICAR60.unique())].sum(axis = 1)
ICAR_60_Norm_data['ICAR16_Total'].describe()
ICAR_60_Norm_data['age'].describe()
#ICAR_60_Norm_data.gender.describe()

for d in codebook_all.dimension.unique():
        dimension_column_names = codebook_all[codebook_all.dimension == d]['ICAR60'].unique()
        ICAR_60_Norm_data_slice = ICAR_60_Norm_data[ICAR_60_Norm_data.columns.intersection(dimension_column_names)]
        dimension_df = pd.DataFrame({d: ICAR_60_Norm_data_slice.sum(axis=1)}, 
                                    index = list(ICAR_60_Norm_data_slice.index))
        dimension_df_60 = pd.DataFrame({f'{d}_60': ICAR_60_Norm_data_slice.sum(axis=1) * (len(dimension_column_names)/4)}, 
                                    index = list(ICAR_60_Norm_data_slice.index))
        ICAR_60_Norm_data = pd.concat([ICAR_60_Norm_data, dimension_df, dimension_df_60], axis = 1)

ICAR_60_Norm_data.columns.intersection(codebook_all.dimension.unique())
ICAR_60_Norm_data['Letter & Number_60'].describe()
ICAR_60_Norm_data['Verbal Reasoning'].describe()
ICAR_60_Norm_data['Matrix Reasoning'].describe()
ICAR_60_Norm_data['3D Rotation_60'].describe()
ICAR_60_Norm_data['ICAR60_Total'] = ICAR_60_Norm_data[[x + "_60" for x in codebook_all.dimension.unique()]].sum(axis = 1)
ICAR_60_Norm_data['ICAR16_Total'].describe()
norm_data_columns = ['age'] + ['ICAR16_Total'] + ['ICAR60_Total'] + codebook_all.dimension.unique().tolist() + [x + "_60" for x in codebook_all.dimension.unique()]
ICAR_Norm_data_use = ICAR_60_Norm_data[norm_data_columns]

ICAR_Norm_data_use.to_csv(os.path.join(codebook_directory, 'ICAR_Norm_Data.csv'), index = False)