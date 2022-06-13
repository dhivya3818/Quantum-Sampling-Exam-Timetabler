from random import sample


def write_to_file(sample, filename, num_days, exams):
    timetable = []
    for k in range(num_days):
        timetable.extend(["{}\t{}\n".format(str(i).zfill(4), k) for i in exams if sample[f'v_{i},{k}'] == 1])

    file = open("output/{}.sol".format(filename), "w")
    file.writelines(timetable)
    file.close()
