import pandas as pd
import os
from pathlib import Path
import glob

def get_file_path(parent_directory, sub_directory):
    """
    Returns the path to the most recent Excel data file for processing,
    and moves it into a subdirectory based on its number of columns.
    """
    data_directory = Path(parent_directory) / sub_directory
    # Get all Excel files in the data directory
    xlsx_files = list(data_directory.glob('*.xlsx'))
    if not xlsx_files:
        raise FileNotFoundError(f"No Excel files found in {data_directory}")
    
    # Sort files by modification time
    xlsx_files.sort(key=lambda x: x.stat().st_mtime)
    most_recent_file_path = xlsx_files[-1]
    
    latest_survey_data_raw = pd.read_excel(most_recent_file_path, skiprows=1)
    most_recent_file_name = most_recent_file_path.name

    num_cols = len(latest_survey_data_raw.columns)
    if num_cols < 50:
        target_subdir = "ICAR 16"
    elif (num_cols > 50) and (num_cols < 120):
        target_subdir = "ICAR 60"
    elif (num_cols > 120) and (num_cols < 300):
        target_subdir = "NEO-IPIP 120"
    elif num_cols > 300:
        target_subdir = "NEO-IPIP 300"
    else:
        raise ValueError("Survey data does not match any expected format based on column count.")

    target_dir = data_directory / target_subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    new_file_path = target_dir / most_recent_file_name

    # Move (rename) the file if not already in the target directory
    if most_recent_file_path.exists() and most_recent_file_path != new_file_path:
        try:
            most_recent_file_path.rename(new_file_path)
        except Exception as e:
            raise IOError(f"Error moving file {most_recent_file_path} to {new_file_path}: {e}")

    # Get the most recent file(s) in the target directory
    xlsx_files_new = list(target_dir.glob('*.xlsx'))
    xlsx_files_new.sort(key=lambda x: x.stat().st_mtime)
    
    if len(xlsx_files_new) < 1:
        raise FileNotFoundError(f"No Excel files found in target directory {target_dir}")
    elif len(xlsx_files_new) == 1:
        most_recent_new_file_path = xlsx_files_new[-1]
        last_file_new_path = xlsx_files_new[-1]
    else:
        most_recent_new_file_path = xlsx_files_new[-1]
        last_file_new_path = xlsx_files_new[-2]
    return str(most_recent_new_file_path), str(last_file_new_path)

def get_survey_info_numeric_data(parent_directory):
    """
    Reads in the latest survey data in Excel format and returns two dataframes:
    one with test information and one with numeric responses.
    """
    latest_survey_data_path, last_survey_data_path = get_file_path(parent_directory=parent_directory, sub_directory='Data')
    latest_survey_data_raw = pd.read_excel(latest_survey_data_path, skiprows=1)
    if latest_survey_data_path == last_survey_data_path:
        latest_survey_data_original = latest_survey_data_raw.copy()
    else:
        last_survey_data = pd.read_excel(last_survey_data_path, skiprows=1)
        latest_survey_data_original = pd.concat([last_survey_data, latest_survey_data_raw]).drop_duplicates(keep=False)

    # Extract test information columns
    if latest_survey_data_original.shape[1] < 15:
        raise ValueError("Not enough columns in the survey data for test information extraction.")
    latest_survey_data_test_info = latest_survey_data_original.iloc[:, [2, 3, 4, 9, 10, 11, 14]].copy()
    latest_survey_data_test_info.rename(columns={
        latest_survey_data_test_info.columns[0]: 'Start Date', 
        latest_survey_data_test_info.columns[1]: 'End Date', 
        latest_survey_data_test_info.columns[2]: 'IP Address'
    }, inplace=True)

    # Combine first, last, and (if present) middle name columns
    if not {'First name', 'Last name'}.issubset(latest_survey_data_original.columns):
        raise ValueError("Expected name columns ('First name', 'Last name') not found in survey data.")
    latest_survey_data_test_info['Full Name'] = (
        latest_survey_data_original['First name'].astype(str) + ' ' +
        latest_survey_data_original['Last name'].astype(str) +
        latest_survey_data_original.get('Middle name', '').fillna('')
    )

    # Calculate response time in minutes
    try:
        response_time_minutes = (
            pd.to_datetime(latest_survey_data_test_info['End Date']) - 
            pd.to_datetime(latest_survey_data_test_info['Start Date'])
        ).dt.total_seconds() / 60
        latest_survey_data_test_info['Response Time'] = pd.to_datetime(response_time_minutes, unit='m').dt.strftime('%H:%M:%S')
    except Exception as e:
        raise ValueError("Error calculating response time: " + str(e))

    # Format completion time (localized to US/Pacific)
    try:
        latest_survey_data_test_info['Completion Time'] = pd.to_datetime(latest_survey_data_test_info['End Date']).dt.tz_localize('US/Pacific').dt.strftime('%m/%d/%Y %I:%M%p %Z')
    except Exception as e:
        raise ValueError("Error formatting completion time: " + str(e))

    # Remove columns with "Unnamed" in their name
    cols_to_drop = list(latest_survey_data_original.filter(regex='Unnamed').columns)
    latest_survey_data_survey = latest_survey_data_original.drop(columns=cols_to_drop)
    
    # Recode string responses to numeric values
    latest_survey_data_numeric = latest_survey_data_survey.replace({
        'Inaccurate': 1, 'Moderately Inaccurate': 2, 
        'Neither': 3, 'Moderately Accurate': 4, 'Accurate': 5
    })

    if latest_survey_data_numeric.shape[1] <= 4:
        raise ValueError("Not enough survey data columns for variance calculation.")
    latest_survey_data_test_info['Response Variance'] = (latest_survey_data_numeric.iloc[:, 4:].std(axis=1) * 10).round(0).astype(float)
    
    return latest_survey_data_test_info, latest_survey_data_numeric
