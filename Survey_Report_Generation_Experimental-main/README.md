# General Description
This repository is intended for the following purposes: 
- To recode survey responses from the following tests: 
    (a) IPIP NEO-120 personality test, 
    (b) IPIP NEO-300 personality test, 
    (c) ICAR-16 cognitive test, and 
    (d) ICAR-60 cognitive test. 
- To generate a survey report for individual responses to each of the tests above. 

## Instructions on Software Needed and Git/Github Usage
To be able to use the code in this repository, please make sure that you have the following as default: 
- Optional but recommended: Have Visual Studio Code (VS Code) installed in your computer. Also install the GitLens extension in your VS Code. 
- If you use PC: Have Conda (either Annaconda or Miniconda) installed and set up in your local computer. 
- Have Git installed in your computer and set up a Git account using your name and email; 
- Clone the current repository from Yi's github (https://github.com/YiLalaWang/Survey_Report_Generation) to a local directory in your computer; preferrably it would be in the same directory as where you save the Data and Report folders. So the directory would have the following sub-directories (Survey_Report_Generation is the current repository):
    - Data
    - Report
    - Survey_Report_Generation
- If you use VS Code, by cloning this repository, it would also automatically link any changes you make to the code to the repository. Please follow the steps below if any changes need to be made:
    - Preferably, please avoid making ANY changes before discussing with Yi. 
    - If you plan to make any changes and that Yi agrees, please create a new branch before starting to make changes, and commit all your changes to this branch. This is so that the code in the Main branch is not influenced by the changing code before the update is done and merged. 
    - After you are done with making, testing, and committing all changes to the new branch, publish the new branch, and go to Yi's github link above to create a pull request for merging the branch. Please add Yi as a reviewer for the pull request such that Yi could review the code with you before approving the merge.
- If Yi wants to make any changes to the code, she will follow the same procedures above as well as having Jason involved before changes are made and during code review in the pull request. 

## Instructions on Environment Setup
The code in this repository is set up with a specific environment (environment_for_survey_repository). The dependencies and pakcages included in this environment are specified in the YML file in the "Environment" folder of this repository. Please follow the instructions in the "Environment_Setup_Instruction.md" file to create the same environment in your computer. 

## Instructions on Workflow for Survey Report Generation
The workflow is designed as follows: 
- All individual response data are exported in "xlsx" format from SurveyMonkey and saved in the "Data" folder. 
    - The program is set up to automatically recognize the latest file from the folder and move it to the corresponding sub-folder. 
    - As such, please export and process **one file at a time** before you export another file. Having multiple files in the Data folder (*excluding those in the subfolders*) may confuse the program.
- Run the "Survey_Report_Generation_Run.py" code to generate individual reports.
- All generated reports are saved in the "Report" folder. 
    - Reports based on responses on personality surveys will be entitled as "Personality_Report_*name of the test taker*.pdf".
    - Reports based on responses on cognitive tests will be entitled as "Cognitive_Report_*name of the test taker*.pdf".