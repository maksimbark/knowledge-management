import csv

def calculateDanger(acc):
    if abs(acc) >= 1.5:
        return 1
    elif abs(acc) >= 0.5:
        return 0.5
    else:
        return 0

currentActionPositive = True

recordNum = 0
recordSum = 0

dangerCoeffNum = 0
dangerCoeffSum = 0
#Stats/2018-07-10-pure_param_stats_driver1.csv
#Stats/2018-06-27-pure_param_stats_driver2.csv
with open("Stats/2018-07-10-pure_param_stats_driver1.csv") as file1:
    reader = csv.DictReader(file1, delimiter=';')
    i = 0
    for line in reader:
        i += 1
        if i == 1:
            recordNum += 1
            recordSum += calculateDanger(float(line["Acceleration(m/s2)"].replace(',','.')))
            currentActionPositive = float(line["AccelerationXYZ"].split(',')[2]) >= 0
        else:
            tmp = float(line["AccelerationXYZ"].split(',')[2]) >= 0
            if tmp != currentActionPositive:
                dangerCoeffNum += 1
                dangerCoeffSum += recordSum / recordNum
                recordSum = 0
                recordNum = 0
                currentActionPositive = tmp

            recordNum += 1
            recordSum += calculateDanger(float(line["Acceleration(m/s2)"].replace(',','.')))
dangerCoeffNum += 1
dangerCoeffSum += recordSum / recordNum

print(dangerCoeffSum / dangerCoeffNum)


