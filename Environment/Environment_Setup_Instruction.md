# General Description
The file(s) in this folder is intended to set up the environment, etc. for processing the code in the Survey_Report_Generation repository. 

# Step-by-Step Guide on Setting up Virtual Environment
## PreRequisites
- You have Git installed and set up properly. 
- You have this repository cloned to your VS Code and synced/pulled the latest changes and files from the repository. 
- You can open the terminal (Terminal in MacOS, or Terminal through conda shell in PC). 
- You should see a "environment_for_survey_report.yml" file in your VS code repository under the "Environment" folder. 

## Preparing Terminal for Installation of environment
- Open the terminal (*Terminal* in your mac, or *"Annoconda Powershell Prompt terminal (Miniconda)"* in your PC)
- In the terminal, use *"cd" + space + path (path needs to be in quotes)* and then hit *return* to navigate and change conda directory to the local path where this yml file is saved in your local folder. 
    - If you use MacOS, you can *"cd"* then drag the "Environment" folder directory into terminal and it will automatically turn into a workable path in your terminal. 
- In conda, type in *conda env list* to check the list of conda environment you have. 
    - It will show a list of currently available environments and their corresponding path/directory.  
    - There should already be a base environment that is installed automatically when you install conda. 
    - Take note of the path of the base directory as this will be needed later. For instance, for me (Yi), the path to the base environment is */opt/miniconda3*.

## Installing Virtual Environment from YML File
- In your conda terminal, type in 
*conda env create -f environment_for_survey_report.yml --prefix [your_conda_base_environment_path]\envs\env_for_survey_report*. Insert the path to your base environment into the brackets (and **do NOT** include the brackets in the actual path).
    - This will automatically create a virtual environment call "env_for_survey_report" in your Conda with all necessary dependencies and packages needed for the survey generation pipeline. It can take 5-10 minutes to finish. 
- The terminal would show something like **done** to suggest that it is done with installation. You can also verify whether the environment is successfully installed by typing *conda env list* in the terminal once the installation process finishes. 
    - If the environment is successfully installed, it would show at least two available environments: *base* and *env_for_survey_report*. 
- You can then activate your new environment by typing into terminal *conda activate env_for_survey_report*. 

## Switch to the Virtual Environment in VS Code
- In your VS Code, simultaneous press *commmand + shift + P* in your MacOS keyboard (or *Ctrl + Shift + P* if you use PC). 
- A dialogue box would appear on the top and you can type in *Python: Select Interpreter*. 
- A list of available interpreters would appear for you to choose what you want to use as the Python interpreter. Choose the option *Python 3.13.0 ('env_for_survey_report')*.
- You will then see *Python 3.13.0 ('env_for_survey_report': conda)* at the bottom right of your VS Code window when you open a Python file in VS Code. And Yay -- **Success**!!!