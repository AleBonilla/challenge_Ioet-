# ACME company, number of employee coincidences in the office in the same period of time

The project below in a programming test for the position of Junior Software Developers and Intern in a recognized company.

------------


The company ACME offers their employees the flexibility to work the hours they want. But due to some external circumstances they need to know what employees have been at the office within the same time frame.

The goal of this exercise is to output a table containing pairs of employees and how often they have coincided in the office.

------------
## Structure of the repository

In the structure of the repository for the main branch we have 2 folders and the main.py, the first folder is **files_acme** where we will find the **acme.txt** which is the supplied data of the ACME company for its subsequent analysis, the second folder is **functions** that contains **functions_ioet.py** archive which contains 9 functions with its due documentation, and finally we have the **main.py** file which is the main file of our project that shows the names of employees with the number of times they have seen in the days and hours of work of each one.

- files_acme
	- acme.txt
- functions
	- functions_ioet.py
- init.py
- main.py


------------

### The functions in the functions_ioet file are:
|Item| Function name|
---- | ----|
|1. | create_dict_general(name_file)|
|2. | manipulate_line(line)|
|3. | create_dict_user(list_days_hours)|
|4. | match_up(dict_general)|
|5. | unique_couples_filter(user_A, user_B, list_Employee_pairs)|
|6. | count_coincidences(dict_days_A, dict_days_B)|
|7. | convert_time_format(hours_A_and_B)|
|8. | add_data(user_A,user_B, coincidences, list_FinalTuples, list_EmployeePairs)|
------------

## Installation and use

You can lower the entire repository and run it locally from its computers, simply with Visual Studio Code, the **main.py** file must be executed directly, this execution will be given by the same vscode terminal since the project does not consist of any graphical interface, in finish can visualize the pairs of unique employees that have been seen in the office and the number of days that were seen, all this from the **acme.txt** text file which is the data for this project.


------------


## **files_acme**
> ### acme.txt

```
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
LUIS=MO15:00-16:00,TU12:00-15:00,TH09:00-11:00,SA13:00-14:00,SU10:00-11:00
ALEJANDRO=MO15:00-17:00,TU12:00-15:00,TH01:00-03:00,SU20:00-21:00
ADRIANA=MO16:00-20:00,TU12:00-18:00,TH07:00-09:45,SU10:00-11:00
FAUSTO=MO10:00-12:00,TU12:00-14:30,TH07:00-11:00,SA14:00-18:15,SU12:00-13:00
PATRICK=MO10:00-10:30,TU12:00-12:30,TH10:00-14:40,SA10:30-12:00
```

## **functions**
> ### functions_ioet.py
```
import datetime

def create_dict_general(name_file):
    dict_general=dict()
    file=open(name_file,"r")
    for line in file:
        user,list_days_hours=manipulate_line(line)
        dict_user=create_dict_user(list_days_hours)
        dict_general[user]=dict_user
    file.close()
    return dict_general

def manipulate_line(line):
    index_equals=line.strip().find("=")
    user=line.strip()[:index_equals]
    list_days_hours=line.strip()[index_equals+1:].split(",")
    return user, list_days_hours

def create_dict_user(list_days_hours):
    dict_user=dict()
    for schedule in list_days_hours:
        day=schedule[:2]
        hours=schedule[2:]
        dict_user[day]=hours
    return dict_user


def match_up(dict_general):
    list_Final_tuples=list()
    list_Employee_pairs=list()
    for user_A,dict_days_A in dict_general.items():
        for user_B,dict_days_B in dict_general.items():
            is_unique=unique_couples_filter(user_A, user_B, list_Employee_pairs)
            if is_unique:
                coincidences=count_coincidences(dict_days_A, dict_days_B)
                list_Final_tuples, list_Employee_pairs=add_data(user_A, user_B, coincidences, list_Final_tuples, list_Employee_pairs)
    return list_Final_tuples

def unique_couples_filter(user_A, user_B, list_Employee_pairs):
    is_unique=user_A!=user_B and (user_A,user_B) not in list_Employee_pairs
    return is_unique 

def count_coincidences(dict_days_A, dict_days_B):
    coincidences=0
    for day_A, hours_A in dict_days_A.items():
        if day_A in dict_days_B:
            hours_B=dict_days_B[day_A]
            hours_A_and_B=hours_A.split("-")+hours_B.split("-")
            start_A, end_A, start_B, end_B=convert_time_format(hours_A_and_B)
            if start_A<=end_B and end_A>=start_B:
                coincidences+=1
    return coincidences
    
def convert_time_format(hours_A_and_B):
    start_A=datetime.datetime.strptime(hours_A_and_B[0],"%H:%M").time()
    start_B=datetime.datetime.strptime(hours_A_and_B[2],"%H:%M").time()
    end_A=datetime.datetime.strptime(hours_A_and_B[1],"%H:%M").time()
    end_B=datetime.datetime.strptime(hours_A_and_B[3],"%H:%M").time()
    return start_A, end_A, start_B, end_B

def add_data(user_A,user_B, coincidences, list_FinalTuples, list_EmployeePairs):
    if coincidences>0:
        list_FinalTuples.append((user_A,user_B,coincidences))
        list_EmployeePairs.append((user_B,user_A))
    return list_FinalTuples, list_EmployeePairs

def show_pairs_with_coincidences(list_Final_tuples):
    for tuple in list_Final_tuples:
        user_A,user_B,coincidences=tuple
        print(f"{user_A}-{user_B}:{coincidences}")
```
## **main.py**
```
from functions.functions_ioet import *
dict_general=create_dict_general("files_acme/acme.txt")
list_FinalTuples=match_up(dict_general)
show_pairs_with_coincidences(list_FinalTuples)
```
