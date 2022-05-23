import datetime

def create_dictGeneral(name_file):
    dict_general=dict()

    file=open(name_file,"r")
    for line in file:
        user,list_days_hours=manipulate_line(line)
        dict_users=create_dictUsers(list_days_hours)
        dict_general[user]=dict_users
    file.close()

    return dict_general

def manipulate_line(line):
    index_equals=line.strip().find("=")
    user=line.strip()[:index_equals]
    list_days_hours=line.strip()[index_equals+1:].split(",")
    return user, list_days_hours

def create_dictUsers(list_days_hours):
    dict_users=dict()
    for item in list_days_hours:
        day=item[:2]
        hours=item[2:]
        dict_users[day]=hours
    return dict_users

#--------------------------------------------------------
def match_up(dict_general):
    list_FinalTuples=list()
    list_EmployeePairs=list()
    for user_A,dict_days_A in dict_general.items():
        for user_B,dict_days_B in dict_general.items():
            condition=uniqueCouples_filter(user_A, user_B, list_EmployeePairs)
            if condition:
                coincidences=count_coincidences(dict_days_A, dict_days_B)
                list_FinalTuples, list_EmployeePairs=add_data(user_A, user_B, coincidences, list_FinalTuples, list_EmployeePairs)
    return list_FinalTuples

def uniqueCouples_filter(user_A, user_B, list_EmployeePairs):
    condition=False
    if user_A!=user_B and (user_A,user_B) not in list_EmployeePairs:
        condition=True
    return condition

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

def show_pairs_with_coincidences(list_FinalTuples):
    for tuple in list_FinalTuples:
        user_A,user_B,coincidences=tuple
        print(f"{user_A}-{user_B}:{coincidences}")