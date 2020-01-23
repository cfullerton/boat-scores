from os import listdir
import csv
###################################################
# Given a sorted csv of scores, returns true if using the high point average score
# system would have changed the results
###################################################
def compare_scoring_systems(file,include_75_rule):
    data = list(csv.reader(open('../scores/' + file)))
    if include_75_rule:
        total_races = len(data[0])
        for boat in data:
            missed_races = 0
            for score in boat[1:]:
                if int(score) == 0:
                    missed_races += 1
            if missed_races / total_races > 0.25:
                for index, score in enumerate(boat):
                    if index != 0:
                        boat[index] = 0
    newdata = []
    for boat in data:
        newdata.append([boat[0]])
    i = 1
    while i < len(data[0]):
        highscore = 0
        for boat in data:
            if int(boat[i]) > int(highscore):
                highscore = int(boat[i])
        j = 0
        for boat in data:
            if int(boat[i]) !=0:
                newdata[j].append(highscore - int(boat[i]) +1)
            else:
                newdata[j].append(0)
            j += 1
        i += 1
    def sumScores(list):
        i=1
        total = 0
        while i < len(list):
            total += list[i]
            i += 1
        return total

    series_scores = []
    for boat in newdata:
        series_scores.append([boat[0],sumScores(boat)])
    series_scores.sort(key=lambda x:x[1],reverse=True)
    compare_index = 0
    top_three_different = False
    while compare_index < 3:
        if data[compare_index][0] != series_scores[compare_index][0]:
            top_three_different = True
        compare_index += 1
    if top_three_different:
        print(data)
        print(newdata)
    return top_three_different

###############################
# runs the results in the scores folder
# through the compare function
###############################
def main(use_75_rule):
    files = listdir('../scores')
    total_changed = 0
    changed_scores = []
    for file in files:
        if compare_scoring_systems(file,use_75_rule):
            changed_scores.append(file)
            total_changed += 1
    if use_75_rule:
        print("with 75% participation rule:")
    else:
        print("without 75% participation rule:")
    print("total changed:",end=" ")
    print(total_changed)
    print("series affected:")
    for series in changed_scores:
        print(series[:-4])
    if not use_75_rule:
        print("Series used in data set:")
        for file in files:
            print(file[:-4])
main(True)
main(False)

