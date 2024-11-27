import requests as rq
from bs4 import BeautifulSoup
import pandas as pd


def set_grades(ses: rq.Session, view_id: list, std_ids: list, grades: list, comment :list):
    """set grades

    Args:
        ses (rq.Session): request session
        view_id (list): exercise view id
        std_ids (list): students ids
        grades (list): students grades
        comment (list): comment for the grades if there
    """
    sesskey, student_dic = get_grading_data(ses, view_id)

    grading_data = {
        "id": view_id,
        "action": "quickgrade",
        "sesskey": sesskey,
        "sendstudentnotifications": "0",
        "_qf__mod_assign_quick_grading_form": "1",
    }

    for student in range(len(std_ids)):
        if std_ids[student] not in student_dic:
            print(std_ids[student], "Not found.")
            continue

        grading_data[f"quickgrade_{student_dic[std_ids[student]]['selector']}"] = grades[student]

        grading_data.update(student_dic[std_ids[student]]["grademodified"])
        grading_data.update(student_dic[std_ids[student]]["gradeattempt"])
        grading_data[
            f"quickgrade_comments_{student_dic[std_ids[student]]['selector']}"
        ] = (comment[student] if comment else "")

    ses.post("https://elearn.squ.edu.om/mod/assign/view.php", data=grading_data)
    return


def get_grading_data(ses: rq.Session, view_id):
    """gets sesskey value that is required for grading post request and
    grading id for every student in the view

    Args:
        ses (rq.Session): request session
        view_id (int): exercise view id

    Returns:
        seskey -> str: session key for login session
        student_dic -> dict:
    """
    grading_url = (
        f"https://elearn.squ.edu.om/mod/assign/view.php?id={view_id}&action=grading"
    )

    grading_page = ses.get(grading_url)

    grading_url_bs4 = BeautifulSoup(grading_page.text, "lxml")
    table = grading_url_bs4.find(
        "table",
        {"class": "flexible table table-striped table-hover generaltable generalbox"},
    ).find("tbody")

    sesskey = grading_url_bs4.find("input", {"name": "sesskey"})["value"]

    # studentId:{selector, grademodified, gradeattempt}
    student_dic = {
        tr.find_all("td")[3].text: {
            "selector": tr["class"][0][4:],
            "grademodified": {
                tr.find_all("input")[1]["name"]: tr.find_all("input")[1]["value"]
            },
            "gradeattempt": {
                tr.find_all("input")[2]["name"]: tr.find_all("input")[2]["value"]
            },
        }
        for tr in table.find_all("tr")
    }
    return sesskey, student_dic


def main():
    ses = rq.Session()
    view_id = input("Enter view id: ")
    file_name = input("Enter file name: ")
    # assuming that username and password are correct
    username = input("Enter username: ")
    password = input("Enter password: ")
    ids_col = input("Enter ids col name: ")
    grades_col = input("Enter grades col name: ")
    comments_col = None
    need_comments = False
    if input("do you want to add comments with grade [y, yes]: ").lower() in ["y", "yes"]:
        need_comments = True
        comments_col = input(
            "Enter comments col name (leave empty if col is next of grades col): "
        )
    if need_comments:
        ids, grades, comments = get_file_grades(
            file_name, ids_col, grades_col, iscomments=True, comments_col_name=comments_col
        )
    else:
        ids, grades, comments = get_file_grades(
            file_name, ids_col, grades_col
        )
    login(ses, username, password)
    set_grades(ses, view_id, ids, grades, comments)


def login(ses: rq.Session, username:str, password:str):
    login_url = "https://elearn.squ.edu.om/login/index.php"
    login_page_req = ses.get(login_url)

    login_page_bs4 = BeautifulSoup(login_page_req.text, "lxml")

    login_token = login_page_bs4.find("input", {"name": "logintoken"})["value"]

    login_data = {
        "logintoken": login_token,
        "username": username,
        "password": password,
    }

    ses.post(login_url, data=login_data)


def get_file_grades(file_name, ids_col_name, grades_col_name, iscomments=False, comments_col_name=None):
    file_extention = file_name.split(".")[1]
    if file_extention == "xlsx":
        df = pd.read_excel(file_name, sheet_name=input("Enter sheet name: "))
    elif file_extention == "csv":
        df = pd.read_csv(file_name)
    df = df.dropna()
    ids_col = df[ids_col_name].astype(int).astype(str).values.tolist()
    grades_col = df[grades_col_name].astype(str).fillna('0').values.tolist()
    if iscomments:
        comments_col = df[list(df)[list(df).index(grades_col_name) + 1]].fillna('').tolist() if not comments_col_name else df[
            comments_col_name].fillna('').tolist()
        return ids_col, grades_col, comments_col

    return ids_col, grades_col, None


main()
