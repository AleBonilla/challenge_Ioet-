from functions.functions_ioet import *

dict_general=create_dictGeneral("files_acme/acme.txt")
print(dict_general)
list_FinalTuples=match_up(dict_general)
show_pairs_with_coincidences(list_FinalTuples)






