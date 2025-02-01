import pandas as pd
import numpy as np
import os
from pathlib import Path

def recode_NEO_IPIP(parent_directory, survey_data):
    """
    This function recodes the items in NEO IPIP 120 and 300 surveys, respectively, into facets and dimensions.

    Args:
        parent_directory (string): string of the parent folder for the code directory.
        survey_data (dataframe): dataframe for all the numeric responses.

    Returns:
        survey_data_reorganize (dataframe): dataframe for all dimension & facet scores. 
        survey_data_personality_score (dataframe): dataframe for the overall personality score. 
        codebook_all: revised codebook with the FFM dimension and facet information. 
    """
    # Find the project path to be able to read the scoring key file
    project_path = Path(parent_directory.parent.absolute())
    codebook_directory = os.path.join(project_path, 'IPIP')
    # Read in the full codebook with both 300 (Full#) and 120 (Short#) keys
    codebook_all = pd.read_excel(os.path.join(codebook_directory, 'Personality Item Key.xlsx'), sheet_name = 'IPIP-NEO-ItemKey')
    # Add a column for the FFM dimensions
    codebook_all['Dimension'] = np.where(codebook_all.Key.str.contains('O'), 'Openness', 
                                         np.where(codebook_all.Key.str.contains('C'), 'Conscientiousness', 
                                                  np.where(codebook_all.Key.str.contains('E'), 'Extroversion', 
                                                           np.where(codebook_all.Key.str.contains('A'), 'Agreeableness', 
                                                                    np.where(codebook_all.Key.str.contains('N'), 'Neuroticism', pd.NA)))))
    # Add a column to mark where recoding is needed because of the minus sign
    codebook_all['Recode'] = np.where(codebook_all.Sign.str.contains('-'), 'Yes', 'No')
    # Trim down to the NEO IPIP 120 and 300 surveys, respectively. 
    codebook_300 = codebook_all[['Dimension', 'Recode', 'Facet', 'Item']]
    codebook_120 = codebook_all.dropna(subset = 'Short#', inplace = False)[['Dimension', 'Recode', 'Facet', 'Item']]
    #len(codebook_120.Key.unique())
    # Recode the survey based on the number of columns
    #survey_data = latest_survey_data_numeric.copy()
    if (len(survey_data.columns) < 300): # - IPIP NEO 120 
        # reversed coded items
        for i in codebook_120.Item.unique():
            if (codebook_120[codebook_120.Item == i]['Recode'].str.contains('Yes').all()):
                survey_data[i] = 6 - survey_data[i]
        
        # calculate average for dimensions
        for d in codebook_all.Dimension.unique():
            dimension_column_names = codebook_120[codebook_120.Dimension == d]['Item'].unique()
            #dimension_column_names = codebook_120[codebook_120.Dimension == 'Openness']['Item'].unique().tolist()
            survey_data_dimension_slice = survey_data[survey_data.columns.intersection(dimension_column_names)]
            dimension_df = pd.DataFrame({d: (survey_data_dimension_slice.sum(axis=1)/len(codebook_120[codebook_120.Dimension == d]['Facet'].unique())).apply(lambda x: round(x, 0))}, 
                                        index = list(survey_data.index))
            survey_data = pd.concat([survey_data, dimension_df], axis = 1)
            
        #survey_data.iloc[:, -5:]
        # Calculate sums for facets
        for f in codebook_120.Facet.unique():
            facet_column_names = codebook_120[codebook_120.Facet == f]['Item'].unique()
            survey_data_facet_slice = survey_data[survey_data.columns.intersection(facet_column_names)]
            facet_df = pd.DataFrame({f: survey_data_facet_slice.sum(axis=1)}, 
                                    index = list(survey_data.index))
            survey_data = pd.concat([survey_data, facet_df], axis = 1)
        
        # reorganize all data such that each dimension is followed by the corresponding facets
        data_reorganize_list = {}
        for d in codebook_all.Dimension.unique():
            dimension_df_split = survey_data[d]
            facet_column_names = codebook_120[codebook_120.Dimension == d]['Facet'].unique()
            facet_df_split = survey_data[survey_data.columns.intersection(facet_column_names)]
            survey_data_dimension = pd.concat([dimension_df_split, facet_df_split], axis = 1)
            data_reorganize_list[d] = survey_data_dimension
        
        survey_data_reorganize = pd.concat(data_reorganize_list, axis = 1)
        survey_data_personality_score = pd.DataFrame({'Personality Score': survey_data[survey_data.columns.intersection(codebook_120.Item.unique())].sum(axis=1)}, 
                                    index = list(survey_data.index))

    elif(len(survey_data.columns) > 300): # - IPIP NEO 300 
        # reversed coded items
        for i in codebook_300.Item.unique():
            if (codebook_120[codebook_300.Item == i]['Recode'].str.contains('Yes').all()):
                survey_data[i] = 6 - survey_data[i]
        
        # calculate sums for dimensions
        for d in codebook_all.Dimension.unique():
            dimension_column_names = codebook_300[codebook_300.Dimension == d]['Item'].unique()
            #dimension_column_names = codebook_120[codebook_120.Dimension == 'Openness']['Item'].unique().tolist()
            survey_data_dimension_slice = survey_data[survey_data.columns.intersection(dimension_column_names)]
            dimension_df = pd.DataFrame({d: (survey_data_dimension_slice.sum(axis=1)/len(codebook_300[codebook_300.Dimension == d]['Facet'].unique())).apply(lambda x: round(x, 0))}, 
                                        index = list(survey_data.index))
            survey_data = pd.concat([survey_data, dimension_df], axis = 1)
            
        # Calculate sums for facets
        for f in codebook_300.Facet.unique():
            facet_item_names = codebook_300[codebook_300.Facet == f]['Item'].unique()
            survey_data_facet_slice = survey_data[survey_data.columns.intersection(facet_item_names)]
            facet_df = pd.DataFrame({f: survey_data_facet_slice.sum(axis=1)}, 
                                    index = list(survey_data.index))
            survey_data = pd.concat([survey_data, facet_df], axis = 1)

        # reorganize all data such that each dimension is followed by the corresponding facets
        data_reorganize_list = {}
        for d in codebook_all.Dimension.unique():
            dimension_df_split = survey_data[d]
            facet_column_names = codebook_300[codebook_300.Dimension == d]['Facet'].unique()
            facet_df_split = survey_data[survey_data.columns.intersection(facet_column_names)]
            survey_data_dimension = pd.concat([dimension_df_split, facet_df_split], axis = 1)
            data_reorganize_list[d] = survey_data_dimension
        
        survey_data_reorganize = pd.concat(data_reorganize_list, axis = 1)
        survey_data_personality_score = pd.DataFrame({'Personality Score': survey_data[survey_data.columns.intersection(codebook_300.Item.unique())].sum(axis=1)}, 
                                    index = list(survey_data.index))

    return survey_data_reorganize, survey_data_personality_score, codebook_all