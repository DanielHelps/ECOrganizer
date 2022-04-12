import os
from drawing_checker import KornitPart

##

def start_organizer(file_list, path, log):
    pop_path = f"{os.getcwd()}\\poppler"
    os.chdir(path)
    # os.chdir("C:\\ECO")
    print(f"Checking folder {os.getcwd()}, These are the findings:")
    # files_list = os.listdir()
    # file_list = ["964-09-75-203_A3.pdf", "964-09-75-203_A3.x_t"]
    # files_set = sorted(set(element[:13] for element in file_list))

    log_location = 1.0
    part_list = []
    counter = -1
    for file in file_list:
        if file[-4:] == ".pdf":
            counter += 1
            part_list.append(KornitPart(file, pop_path, file_list, log, log_location))
            part_list[counter].compare_drawing_numbers()
            part_list[counter].compare_revs()
            part_list[counter].check_signatures()
            part_list[counter].check_date()
            log_location+=1.0
    # [centers_x, centers_y] = detect_circles(files[8])
    pass
    # for single_file in files:
    #     if single_file[len(single_file)-4:] == ".pdf":
    #         drawing_checker.find_drawing_number(single_file)
    #         drawing_checker.find_rev(single_file)
    # pass
    return part_list
    ##
    # for one_file in files_set:
    #     check_occurrences(one_file, files)
    #     check_revs(one_file, files)
