# eLearingGradeBot
eLearingGradeBot is a tool to automate the insertion of grades to squ elearing system from csv or xlsx file.

# How to install
* First you need to install python.
* clone repo and install requirements
    ```bash
    git clone https://github.com/Mohammed-Alabri/eLearingGradeBot
    cd eLearingGradeBot
    pip install -r requirements.txt
    ```
# How to run
* run it as any python code
    ```bash
    python3 main.py
    ```
* when run it program need the following
    * View id: view id of the exercise, it's in the url of the exercise. Example:
        ```https://elearn.squ.edu.om/mod/assign/view.php?id=123456```
        * view id is ```123456```
    * File name: file name of the grades sheet. (if it's xlsx, sheet name is needed).
    * elearing username (for authentication).
    * elearing password (for authentication).
    * ids column name.
    * grades column name.
* Example:
    ```
    Enter view id: 1234567
    Enter file name: sheet.xlsx
    Enter username: s123456
    Enter password: blablab
    Enter ids col name: Student Id.
    Enter grades col name: Lab2W3
    do you want to add comments with grade [yes]: yes
    Enter comments col name (leave empty if col is next of grades col):
    Enter sheet name: Section_21
    ```
# Notes
* tool still in development.
* for educational purposes.
