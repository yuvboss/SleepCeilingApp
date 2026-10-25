from storage import DAYS
from time_helpers import duration 

#Sleep Calculation function:
def SleepCalculation(week):
    #nights list with sleep for each night
    nights = [] 
    #Loop for each day in the week
    for day in DAYS:
        #end time lists
        ends = []
        #loop for number of activities
        for activities in week["activities"]:
            if day in activities["days"]:
                end = activities["end"] + (DAYS.index(day)*24*60)
                if activities["end"] < activities["start"]:
                    end = activities["end"] + ((DAYS.index(day)+1)*24*60)
                ends.append(end)
        if len(ends) > 0:
            latestTime = max(ends)
        #print(day, ends)
        if day != "Sun":
            nextDay = DAYS.index(day) + 1
            numToWord = DAYS[nextDay]
            wake = week["wake"][numToWord]+(DAYS.index(numToWord)*24*60)
        if day == "Sun":
            wake = week["wake"]["Mon"]+(7*24*60)
        if len(ends) > 0:
            nights.append(wake-latestTime) 
        else:
            nights.append(None)
    Last = nights.pop()
    nights.insert(0,Last)
    return nights
if __name__ == "__main__":
    test_week = {
        "wake": {"Mon":420, "Tue":420,"Wed":420, "Thu":420,"Fri":420, "Sat":600, "Sun":600},
        "activities": [ 
            {"name": "School", "days": ["Mon","Tue","Wed","Thu","Fri"], "start": 480, "end": 900, "importance": 5, "malleable": False},
            {"name": "Homework", "days": ["Mon","Tue"], "start": 1260, "end": 1380, "importance": 3, "malleable": False},
            {"name": "Shift", "days": ["Fri"], "start": 1320, "end": 30, "importance": 4, "malleable": False},
        ],
    }
    print(SleepCalculation(test_week))