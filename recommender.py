import copy
from sleep_calc import SleepCalculation
from time_helpers import duration
from storage import DAYS

Loss = 0
def Importance(activity):
    timeTaken = duration(activity["start"],activity["end"])
    if activity["importance"] == 1: 
        Loss = timeTaken
    if activity["importance"] == 2: 
        activity["end"] = round(activity["start"] + timeTaken*0.25)
        Loss = round(timeTaken*0.75)
    if activity["importance"] == 3: 
        activity["end"] = round(activity["start"] + timeTaken*0.5)
        Loss = round(timeTaken*0.5)
    if activity["importance"] == 4: 
        activity["end"] = round(activity["start"] + timeTaken*0.75)
        Loss = round(timeTaken*0.25)
    if activity["importance"] == 5: 
        activity["end"] = activity["start"] + timeTaken
        Loss = 0
    return(Loss)
    
          

def recommend(week):
    newWeek = copy.deepcopy(week)
    shortNights = []
    for i, check in enumerate(SleepCalculation(newWeek)):
        if check == None:
            pass
        elif 0 < check < 510:
            if i!= 0:
                shortNights.append((DAYS[i-1], DAYS[i], check))
            else:
                shortNights.append((DAYS[6], DAYS[i], check))
    trimmedActivities = []
    for day in shortNights:
        for activity in newWeek["activities"]:
            if day[0] in activity["days"] and activity not in trimmedActivities:
                change = Importance(activity)
                for thing in newWeek["activities"]:
                    if thing["malleable"] == True and thing["start"] >= activity["end"]:
                        thing["start"] -= change
                        thing["end"] -= change
                if activity["importance"] == 1:
                    newWeek["activities"].remove(activity)
                trimmedActivities.append(activity)
    return(newWeek)



    


# Test week: only runs with `venv/bin/python recommender.py`, never in the app.
# Wake 6:40 on weekdays, 9:00 at the weekend.
#   School    Mon-Fri 08:00-15:00  importance 5 (never touched)
#   Practice  Mon, Wed 16:00-18:30  importance 4, movable
#   Homework  Sun-Thu 20:30-23:00   importance 3, movable
#   Phone     every day 23:00-23:45 importance 1, movable (can be cut)
# Predicted sleep by morning: Mon-Fri 415 min (6h 55m, short), Sat and Sun 555 min (fine).
if __name__ == "__main__":
    test_week = {
        "wake": {"Mon": 400, "Tue": 400, "Wed": 400, "Thu": 400, "Fri": 400, "Sat": 540, "Sun": 540},
        "wake_default": 400,
        "activities": [
            {"name": "School", "days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "start": 480, "end": 900, "importance": 5, "malleable": False},
            {"name": "Practice", "days": ["Mon", "Wed"], "start": 960, "end": 1110, "importance": 4, "malleable": True},
            {"name": "Homework", "days": ["Sun", "Mon", "Tue", "Wed", "Thu"], "start": 1230, "end": 1380, "importance": 3, "malleable": True},
            {"name": "Phone", "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "start": 1380, "end": 1425, "importance": 1, "malleable": True},
        ],
    }
    print("Predicted before:", SleepCalculation(test_week))
    print("recommend:", recommend(test_week))
