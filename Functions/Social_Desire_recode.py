import pandas as pd
import numpy as np
import os
from pathlib import Path

def recode_SDS(parent_directory, survey_data):
    """
    Code to generate the social desirability scores for each test taker. 

    Args:
        parent_directory (string): string of the parent folder for the code directory.
        survey_data (dataframe): dataframe for all the numeric responses.
    
    Returns:
        SDS_df (dataframe): dataframe with the social desirability score. 
    """
    project_path = Path(parent_directory.parent.absolute())
    codebook_directory = os.path.join(project_path, 'IPIP')
    # Read in the full codebook with both 300 (Full#) and 120 (Short#) keys
    codebook = pd.read_excel(os.path.join(codebook_directory, 'Personality Item Key.xlsx'), sheet_name = 'Social_Desirability')
    survey_data_SDS_slice = survey_data[survey_data.columns.intersection(codebook.Item.unique())]
    SDS_df = pd.DataFrame({'Social Desirability Score': survey_data_SDS_slice.sum(axis=1)}, index = list(survey_data.index))
    return SDS_df

    