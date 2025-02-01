import pandas as pd
from pathlib import Path

def recode_SDS(parent_directory, survey_data):
    """
    Generates the social desirability scores for each test taker.
    
    Args:
        parent_directory (str or Path): Parent folder for the repository.
        survey_data (DataFrame): DataFrame containing the numeric responses.
    
    Returns:
        SDS_df (DataFrame): DataFrame with the computed social desirability score.
    """
    project_path = Path(parent_directory).parent
    codebook_directory = project_path / 'IPIP'
    codebook_file = codebook_directory / 'Personality Item Key.xlsx'
    if not codebook_file.exists():
        raise FileNotFoundError(f"Codebook not found: {codebook_file}")
    codebook = pd.read_excel(codebook_file, sheet_name='Social_Desirability')
    survey_data_SDS_slice = survey_data[survey_data.columns.intersection(codebook.Item.unique())]
    SDS_df = pd.DataFrame({'Social Desirability Score': survey_data_SDS_slice.sum(axis=1)}, index=survey_data.index)
    return SDS_df
