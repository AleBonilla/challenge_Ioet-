import datetime

def create_dict_general(name_file):
    '''

    This function will read the file name_file and by filtering all its data it will 
    create the general dictionary in which the structure will be: 
    dict_general={user1:{'day1':'check_in_time:departure_time',..},...}
    
        Args:
                name_file(string): The name of the file to read
                 
        Returns:
                dict_general(dict): Returns the dictionary already with all the data of the file name_file

    '''
    dict_general=dict()

    file=open(name_file,"r")
    for line in file:
        user,list_days_hours=manipulate_line(line)
        dict_user=create_dict_user(list_days_hours)
        dict_general[user]=dict_user
    file.close()

    return dict_general

def manipulate_line(line):
    '''

    The function takes as an argument a text string of a specific user with their schedules for the different days, 
    when manipulating the text string, it will return only the user's name and a list with the days and their entry 
    and exit times. Line example: 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
    
        Args:
                line(string): Text string to manipulate
                 
        Returns:
                user(string): Returns the username
                list_days_hours(list): Returns a list with the days and their entry and exit times

    '''
    index_equals=line.strip().find("=")
    user=line.strip()[:index_equals]
    list_days_hours=line.strip()[index_equals+1:].split(",")
    return user, list_days_hours

def create_dict_user(list_days_hours):
    '''
    
    This function takes as an argument a list of a specific user with the format: 
    ['MO10:00-12:00', 'TH12:00-14:00', 'SU20:00-21:00',..].
    When manipulating the list, it returns a dictionary that will have the prefixes of 
    the days as keys and the entry and exit times of the days as values:
    dict_user:{'day1':'check_in_time:departure_time',..}.
    
        Args:
                list_days_hours(list): List with the days and their entry and exit times
                 
        Returns:
                dict_user(dict): Returns a dictionary of a user with the data of the entry and exit times of the different days

    '''
    dict_user=dict()
    for schedule in list_days_hours:
        day=schedule[:2]
        hours=schedule[2:]
        dict_user[day]=hours
    return dict_user


def match_up(dict_general):
    '''

    This function takes as an argument the dictionary created in the create_dict_general() function, 
    when manipulated it will return a final list containing tuples of three values, those three values 
    will be user1, user 2, and the times they were seen on all days who went to work.
    
        Args:
                dict_general(dict): The dictionary created in the create_dict_general() with users and their work schedules
                 
        Returns:
                list_Final_tuples(list): Return a final list containing tuples of three values (user1,user2,coincidences)

    '''
    list_Final_tuples=list()
    list_Employee_pairs=list()
    for user_A,dict_days_A in dict_general.items():
        for user_B,dict_days_B in dict_general.items():
            is_unique=unique_couples_filter(user_A, user_B, list_Employee_pairs)
            if is_unique:
                coincidences=count_coincidences(dict_days_A, dict_days_B)
                list_Final_tuples, list_Employee_pairs=add_data(user_A, user_B, coincidences, list_Final_tuples, list_Employee_pairs)
    return list_Final_tuples

def unique_couples_filter(user_A, user_B, list_EmployeePairs):
    '''

    The function takes as arguments two usernames and a list of existing partners, and returns the 
    truth value with the condition that the users must not be the same person and also must not exist 
    as partners in the list of existing partners.

        Args:
                user_A(string): Username A
                user_B(string): Username B
                list_EmployeePairs(list): List of existing partners
                 
        Returns:
                is_unique(bool): Returns the truth value that they are unique

    '''
    is_unique=user_A!=user_B and (user_A,user_B) not in list_EmployeePairs
    return is_unique
  

def count_coincidences(dict_days_A, dict_days_B):
    '''

    This function receives the dictionary of user A and B, and it will go through both dictionaries to 
    finally return the number of times that both users saw each other in the exact days and hours that 
    they went to the office.

        Args:
                dict_days_A(dict): Dictionary with user A's schedule
                dict_days_B(dict): Dictionary with user B's schedule
                 
        Returns:
                coincidences(int): Returns the number of coincidences that both users had in the office

    '''
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
    '''

    This function receives a text string that contains the check-in and check-out times for user A 
    and user B, and returns the check-in and check-out times separately for user A and user B, in 
    time format thanks to the datetime library.

        Args:
                hours_A_and_B(string): Text string containing the check-in and check-out times of user A and B
                 
        Returns:
                start_A(datetime.time): Returns the check-in time of user A in time format
                start_B(datetime.time): Returns the check-in time of user B in time format
                end_A(datetime.time): Returns the check-out time of user A in time format
                end_B(datetime.time): Returns the check-out time of user B in time format

    '''
    start_A=datetime.datetime.strptime(hours_A_and_B[0],"%H:%M").time()
    start_B=datetime.datetime.strptime(hours_A_and_B[2],"%H:%M").time()
    end_A=datetime.datetime.strptime(hours_A_and_B[1],"%H:%M").time()
    end_B=datetime.datetime.strptime(hours_A_and_B[3],"%H:%M").time()
    return start_A, end_A, start_B, end_B

def add_data(user_A,user_B, coincidences, list_FinalTuples, list_EmployeePairs):
    '''

    This function receives as arguments the usernames A and B, the number of matches they had in their work schedules, 
    the final list of tuples, and the list of unique pairs, the function will return the final list of final tuples and 
    the list of modified unique pairs, if the coincidences that those two users had is greater than 0.

        Args:
                user_A(string): Username A
                user_B(string): Username B
                coincidences(int): The number of coincidences that both users had in the office
                list_FinalTuples(list): Final list containing tuples of three values (user1,user2,coincidences)
                list_EmployeePairs(list): List of existing partners
                 
        Returns:
                list_FinalTuples(list): Return the modified list containing tuples of three values
                list_EmployeePairs(list): Return the modified list of existing partners
                

    '''
    if coincidences>0:
        list_FinalTuples.append((user_A,user_B,coincidences))
        list_EmployeePairs.append((user_B,user_A))
    return list_FinalTuples, list_EmployeePairs

def show_pairs_with_coincidences(list_Final_tuples):
    '''

    The function takes as an argument the final list of tuples where each tuple has user A, user B and the number of 
    times they saw each other in the office during their schedules, it does not return anything but it displays the 
    three data on the screen with a good view format:

        Args:
                list_Final_tuples(list): Final list containing tuples of three values (user1,user2,coincidences)       

    '''
    for tuple in list_Final_tuples:
        user_A,user_B,coincidences=tuple
        print(f"{user_A}-{user_B}:{coincidences}")