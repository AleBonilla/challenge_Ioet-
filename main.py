from functions.functions_ioet import *

dict_general=create_dict_general("files_acme/acme.txt")
list_FinalTuples=match_up(dict_general)
show_pairs_with_coincidences(list_FinalTuples)

