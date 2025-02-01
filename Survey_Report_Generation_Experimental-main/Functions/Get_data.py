import pandas as pd
#import numpy as np
import os
from os import walk
from pathlib import Path
import glob

def get_file_path(parent_directory, sub_directory):
    """
    This function returns the path to the most recent data file.
    parent_directory (string): directory of the parent folder of the current repository.

    return: 
    most_recent_new_file_path (string): path of the most recently exported data to be processed. 
    last_file_new_path (string): path of the last processed data.
    """
    data_directory = os.path.join(parent_directory, sub_directory)
    # read the excel file in the data directory
    xlsx_files = [file for file in glob.glob(os.path.join(data_directory, '*.xlsx'))]
    # get the most recently modified data file in the Data folder
    xlsx_files.sort(key=os.path.getmtime)
    most_recent_file_path = xlsx_files[-1]
    latest_survey_data_raw = pd.read_excel(most_recent_file_path, skiprows = 1)
    most_recent_file_name = most_recent_file_path.replace(data_directory + '/', '')
    # move file to its corresponding sub-directory
    if(len(latest_survey_data_raw.columns) < 50): 
        os.rename(most_recent_file_path, data_directory + '/ICAR 16/' + most_recent_file_name)
        new_file_path = data_directory + '/ICAR 16/' + most_recent_file_name
    elif((len(latest_survey_data_raw.columns) > 50) & (len(latest_survey_data_raw.columns) < 120)): 
        os.rename(most_recent_file_path, data_directory + '/ICAR 60/' + most_recent_file_name)
        new_file_path = data_directory + '/ICAR 60'
    elif((len(latest_survey_data_raw.columns) > 120) & (len(latest_survey_data_raw.columns) < 300)): 
        os.rename(most_recent_file_path, data_directory + '/NEO-IPIP 120/' + most_recent_file_name)
        new_file_path = data_directory + '/NEO-IPIP 120'
    elif(len(latest_survey_data_raw.columns) > 300): 
        os.rename(most_recent_file_path, data_directory + '/NEO-IPIP 300/' + most_recent_file_name)
        new_file_path = data_directory + '/NEO-IPIP 300'
    
    # get the most recently modified data file in the new file path
    xlsx_files_new = [file for file in glob.glob(os.path.join(new_file_path, '*.xlsx'))]
    # get the most recently modified data file in the Data folder
    xlsx_files_new.sort(key=os.path.getmtime)
    if(len(xlsx_files_new) < 2): 
        most_recent_new_file_path = xlsx_files_new[-1]
        last_file_new_path = xlsx_files_new[-1]
    else: 
        most_recent_new_file_path = xlsx_files_new[-1]
        last_file_new_path = xlsx_files_new[-2]
    return most_recent_new_file_path, last_file_new_path


def get_survey_info_numeric_data(parent_directory):
    # Use the function defined in "Get_data.py" to read in the latest survey data in Excel format
    latest_survey_data_path, last_survey_data_path = get_file_path(parent_directory = parent_directory, sub_directory = 'Data')
    # Read in excel data (skip first row which does not contain actual items) for both latest and last processed data
    latest_survey_data_raw = pd.read_excel(latest_survey_data_path, skiprows = 1)
    # when there is only one excel file in the directory, just use the data in that excel file.
    if (latest_survey_data_path == last_survey_data_path): 
        latest_survey_data_original = latest_survey_data_raw.copy()
    else: 
        last_survey_data = pd.read_excel(last_survey_data_path, skiprows = 1)
        # get the latest data by removing rows that duplicate from the previously processed data
        latest_survey_data_original = pd.concat([last_survey_data, latest_survey_data_raw]).drop_duplicates(keep=False)

    # Get dataframe with survey data test information ##########
    # extract the first few columns with test information (start/end date, IP address)
    latest_survey_data_test_info = latest_survey_data_original.iloc[:, [2, 3, 4, 9, 10, 11, 14]]
    latest_survey_data_test_info.rename(columns = {latest_survey_data_test_info.columns[0]: 'Start Date', 
                                                latest_survey_data_test_info.columns[1]: 'End Date', 
                                                latest_survey_data_test_info.columns[2]: 'IP Address'}, inplace = True)

    # combine first and last name
    latest_survey_data_test_info['Full Name'] = latest_survey_data_test_info['First name'] + ' ' + latest_survey_data_test_info['Last name'] + latest_survey_data_test_info['Middle name'].fillna('')

    # calculate response time in minutes
    latest_survey_data_test_info['Response Time'] = pd.to_datetime((latest_survey_data_test_info['End Date'] - latest_survey_data_test_info['Start Date']).dt.total_seconds()/60, 
                                                                unit='m').dt.strftime('%H:%M:%S')

    latest_survey_data_test_info['Completion Time'] = pd.to_datetime(latest_survey_data_test_info['End Date'], unit = 's', utc = False).dt.tz_localize('US/Pacific').dt.strftime('%m/%d/%Y %I:%M%p %Z')

    # Get dataframe with numeric responses ###########
    # Get rid of columns with "unnamed" to form the dataframe for survey data only
    latest_survey_data_survey = latest_survey_data_original[latest_survey_data_original.columns.drop(list(latest_survey_data_original.filter(regex='Unnamed')))]
    # Recode the string responses to numeric values
    with pd.option_context("future.no_silent_downcasting", True):
        latest_survey_data_numeric = latest_survey_data_survey.replace({'Inaccurate': 1, 'Moderately Inaccurate': 2, 
                                                                'Neither': 3, 'Moderately Accurate': 4, 'Accurate': 5})
    # calculate variance by survey data responses
    latest_survey_data_test_info['Response Variance'] = (latest_survey_data_numeric.iloc[:, 4:].std(axis = 1)*10).astype(float).round(0)
    
    return latest_survey_data_test_info, latest_survey_data_numeric


