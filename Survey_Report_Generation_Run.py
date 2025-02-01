#!/usr/bin/env python3
"""
Updated Survey_Report_Generation_Run.py:
Processes individual responses, recodes them, and generates PDF reports.
The main logic is protected by a main guard.
"""

import pandas as pd
from pathlib import Path
import kaleido  # Ensure kaleido is installed and compatible

from Functions.Get_data import get_survey_info_numeric_data
from Functions.NEO_IPIP_recode import recode_NEO_IPIP
from Functions.Social_Desire_recode import recode_SDS
#from Functions.ICAR_recode import *  # Currently not in use
from Functions.Personality_Report_Generation import personality_report_generation

def main():
    # Set up the working directory using pathlib
    code_directory = Path.cwd()
    parent_directory = code_directory.parent

    # Retrieve both test info and numeric survey data
    latest_survey_data_test_info, latest_survey_data_numeric = get_survey_info_numeric_data(parent_directory=parent_directory)

    if len(latest_survey_data_numeric.columns) > 70:  # IPIP NEO 120 or NEO 300 survey
        # Recode personality survey data
        survey_data_numeric_calculate, survey_data_personality_score, codebook_all = recode_NEO_IPIP(
            parent_directory=parent_directory, survey_data=latest_survey_data_numeric)
        
        # If the dataframe has a multi-index, flatten it
        if hasattr(survey_data_numeric_calculate.columns, 'get_level_values'):
            survey_data_numeric_calculate.columns = survey_data_numeric_calculate.columns.get_level_values(1)
        
        survey_data_SDS = recode_SDS(parent_directory=parent_directory, survey_data=latest_survey_data_numeric)
        merge_cols = ['Full Name', 'Response Time', 'Completion Time', 'Email address', 'Response Variance']
        survey_data_numeric_calculate_concat = pd.concat([
            latest_survey_data_test_info[merge_cols],
            survey_data_SDS,
            survey_data_personality_score,
            survey_data_numeric_calculate
        ], axis=1)
        
        # Generate individual reports for each test taker
        for name in survey_data_numeric_calculate_concat['Full Name'].unique():
            original_individual_data = survey_data_numeric_calculate_concat[survey_data_numeric_calculate_concat['Full Name'] == name]
            original_individual_data_t = original_individual_data.transpose()
            # Use the first row as header
            original_individual_data_t.columns = original_individual_data_t.iloc[0]
            original_individual_data_t = original_individual_data_t.drop(original_individual_data_t.index[0])
            original_individual_data_t['Facet'] = original_individual_data_t.index
            # Merge with codebook to bring in Dimension and Facet information
            original_individual_data_t_merge = original_individual_data_t.merge(
                codebook_all[['Dimension', 'Facet']].drop_duplicates(), how='left', on='Facet')
            
            item_number = 120 if (len(latest_survey_data_numeric.columns) < 200) else 300
            report = personality_report_generation(
                test_taker_df=original_individual_data_t_merge, name=name, item_number=item_number)
            
            output_path = parent_directory / "Report" / f"Personality_Report_{name}.pdf"
            report.write_image(str(output_path), engine='kaleido')
    else:
        # Placeholder for handling ICAR data
        print("ICAR survey handling not implemented yet.")

if __name__ == '__main__':
    main()


