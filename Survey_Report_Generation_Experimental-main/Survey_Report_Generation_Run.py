"""
This code is the "Master file" to process individual responses, recode them, 
and generate the corresponding PDF report. 
"""

import pandas as pd
import os
from pathlib import Path
import kaleido

from Functions.Get_data import *
from Functions.NEO_IPIP_recode import *
from Functions.Social_Desire_recode import *
#from Functions.ICAR_recode import *
from Functions.Personality_Report_Generation import *

# need to initiate the interpreter from the current Python script. Otherwise it will mess up the cwd.
code_directory = os.getcwd() 
path_current = Path(code_directory)
# Find the parent folder of the code directory to be able to read data files
parent_directory = Path(path_current.parent.absolute())

# get both test info and numeric data
latest_survey_data_test_info, latest_survey_data_numeric = get_survey_info_numeric_data(parent_directory = parent_directory)

if (len(latest_survey_data_numeric.columns) > 70): # - IPIP NEO 120 or IPIP NEO 300 
    # calculate personality dimensions/facets scores
    survey_data_numeric_calculate, survey_data_personality_score, codebook_all = recode_NEO_IPIP(parent_directory = parent_directory, survey_data = latest_survey_data_numeric)
    survey_data_numeric_calculate.columns = survey_data_numeric_calculate.columns.get_level_values(1)
    survey_data_SDS = recode_SDS(parent_directory = parent_directory, survey_data = latest_survey_data_numeric) 
    # merge the test info and dimension/facet dataframes
    survey_data_numeric_calculate_concat = pd.concat([latest_survey_data_test_info[['Full Name', 'Response Time', 'Completion Time', 'Email address', 'Response Variance']], 
                                                      survey_data_SDS, survey_data_personality_score, survey_data_numeric_calculate], axis = 1)
    # extract the scores for each test taker 
    for name in survey_data_numeric_calculate_concat['Full Name'].unique():
        original_individual_data = survey_data_numeric_calculate_concat[survey_data_numeric_calculate_concat['Full Name'] == name]
        original_individual_data_t = original_individual_data.transpose()
        original_individual_data_t.columns = original_individual_data_t.iloc[0]
        original_individual_data_t = original_individual_data_t.drop(original_individual_data_t.index[0])
        original_individual_data_t['Facet'] = original_individual_data_t.index
        original_individual_data_t_merge = original_individual_data_t.merge(codebook_all[['Dimension', 'Facet']].drop_duplicates(), how = 'left', on = 'Facet')
        # generate report with plotly
        report = personality_report_generation(test_taker_df = original_individual_data_t_merge, name = name, 
                                               item_number = 120 if (len(latest_survey_data_numeric.columns) < 200) else 300)
        report.write_image(os.path.join(parent_directory, f"Report/Personality_Report_{name}.pdf"), engine = 'kaleido')

    

#else: # - ICARS 16 or ICAR 60
    


