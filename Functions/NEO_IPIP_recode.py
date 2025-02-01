import pandas as pd
import numpy as np
from pathlib import Path

def recode_NEO_IPIP(parent_directory, survey_data):
    """
    Recodes the items in the NEO IPIP 120 and 300 surveys into facets and dimensions.
    """
    project_path = Path(parent_directory).parent
    codebook_directory = project_path / 'IPIP'
    codebook_file = codebook_directory / 'Personality Item Key.xlsx'
    if not codebook_file.exists():
        raise FileNotFoundError(f"Codebook not found: {codebook_file}")
    codebook_all = pd.read_excel(codebook_file, sheet_name='IPIP-NEO-ItemKey')
    
    # Add FFM dimension based on Key content
    codebook_all['Dimension'] = np.where(codebook_all.Key.str.contains('O'), 'Openness', 
                                  np.where(codebook_all.Key.str.contains('C'), 'Conscientiousness', 
                                  np.where(codebook_all.Key.str.contains('E'), 'Extroversion', 
                                  np.where(codebook_all.Key.str.contains('A'), 'Agreeableness', 
                                  np.where(codebook_all.Key.str.contains('N'), 'Neuroticism', pd.NA)))))
    # Mark items that require reverse coding
    codebook_all['Recode'] = np.where(codebook_all.Sign.str.contains('-'), 'Yes', 'No')
    
    # Create separate codebooks for 300-item and 120-item surveys
    codebook_300 = codebook_all[['Dimension', 'Recode', 'Facet', 'Item']].copy()
    codebook_120 = codebook_all.dropna(subset=['Short#']).copy()[['Dimension', 'Recode', 'Facet', 'Item']]
    
    if len(survey_data.columns) < 300:  # NEO IPIP 120
        for i in codebook_120.Item.unique():
            if codebook_120[codebook_120.Item == i]['Recode'].str.contains('Yes').all():
                survey_data[i] = 6 - survey_data[i]
        
        # Calculate average scores for dimensions
        for d in codebook_all.Dimension.unique():
            dimension_items = codebook_120[codebook_120.Dimension == d]['Item'].unique()
            survey_data_slice = survey_data[survey_data.columns.intersection(dimension_items)]
            if len(dimension_items) > 0:
                dimension_df = pd.DataFrame({d: (survey_data_slice.sum(axis=1) / 
                    len(codebook_120[codebook_120.Dimension == d]['Facet'].unique())).round(0)},
                    index=survey_data_slice.index)
                survey_data = pd.concat([survey_data, dimension_df], axis=1)
            
        # Sum facets
        for f in codebook_120.Facet.unique():
            facet_items = codebook_120[codebook_120.Facet == f]['Item'].unique()
            survey_data_slice = survey_data[survey_data.columns.intersection(facet_items)]
            facet_df = pd.DataFrame({f: survey_data_slice.sum(axis=1)}, index=survey_data.index)
            survey_data = pd.concat([survey_data, facet_df], axis=1)
        
        # Reorganize: each dimension followed by its facets
        data_reorganize_list = {}
        for d in codebook_all.Dimension.unique():
            dimension_series = survey_data[d]
            facet_items = codebook_120[codebook_120.Dimension == d]['Facet'].unique()
            facet_df = survey_data[survey_data.columns.intersection(facet_items)]
            data_reorganize_list[d] = pd.concat([dimension_series, facet_df], axis=1)
        
        survey_data_reorganize = pd.concat(data_reorganize_list, axis=1)
        survey_data_personality_score = pd.DataFrame({'Personality Score': survey_data[survey_data.columns.intersection(codebook_120.Item.unique())].sum(axis=1)},
                                                      index=survey_data.index)
    elif len(survey_data.columns) > 300:  # NEO IPIP 300
        # Use codebook_300 for reverse coding
        for i in codebook_300.Item.unique():
            if codebook_300[codebook_300.Item == i]['Recode'].str.contains('Yes').all():
                survey_data[i] = 6 - survey_data[i]
        
        # Calculate sums for dimensions
        for d in codebook_all.Dimension.unique():
            dimension_items = codebook_300[codebook_300.Dimension == d]['Item'].unique()
            survey_data_slice = survey_data[survey_data.columns.intersection(dimension_items)]
            if len(dimension_items) > 0:
                dimension_df = pd.DataFrame({d: (survey_data_slice.sum(axis=1) / 
                    len(codebook_300[codebook_300.Dimension == d]['Facet'].unique())).round(0)},
                    index=survey_data_slice.index)
                survey_data = pd.concat([survey_data, dimension_df], axis=1)
            
        # Sum facets
        for f in codebook_300.Facet.unique():
            facet_items = codebook_300[codebook_300.Facet == f]['Item'].unique()
            survey_data_slice = survey_data[survey_data.columns.intersection(facet_items)]
            facet_df = pd.DataFrame({f: survey_data_slice.sum(axis=1)}, index=survey_data.index)
            survey_data = pd.concat([survey_data, facet_df], axis=1)

        # Reorganize: each dimension followed by its facets
        data_reorganize_list = {}
        for d in codebook_all.Dimension.unique():
            dimension_series = survey_data[d]
            facet_items = codebook_300[codebook_300.Dimension == d]['Facet'].unique()
            facet_df = survey_data[survey_data.columns.intersection(facet_items)]
            data_reorganize_list[d] = pd.concat([dimension_series, facet_df], axis=1)
        
        survey_data_reorganize = pd.concat(data_reorganize_list, axis=1)
        survey_data_personality_score = pd.DataFrame({'Personality Score': survey_data[survey_data.columns.intersection(codebook_300.Item.unique())].sum(axis=1)},
                                                      index=survey_data.index)
    
    return survey_data_reorganize, survey_data_personality_score, codebook_all
