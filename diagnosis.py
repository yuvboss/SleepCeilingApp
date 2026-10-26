from flow import send_back_to_week, go_to_good_job, go_to_updated_schedule
import streamlit as st
@st.dialog("No Sleep Entered!")
def my_popup():
    st.write("Enter an actual amount of sleep before proceeding.")
def Conditions(predicted, actual):
    compareOne = []
    compareTwo = []
    for goal in predicted:
        if goal == None:
            compareOne.append(True)
        elif goal >= 510:
            compareOne.append(True)
        else:
            compareOne.append(False)
    for real in actual: 
        if real == None:
            my_popup()
            st.stop()
        elif real*60 >= 510:
            compareTwo.append(True)
        else:
            compareTwo.append(False)
    if all(compareOne) and all(compareTwo):
        go_to_good_job()
    elif compareOne != compareTwo:
        send_back_to_week("Your predicted sleep and actual sleep don't match! Enter all your activities before proceeding")
    else:
        go_to_updated_schedule()
        
    
        

"""
if __name__ == "__main__":
    pred_green = [540, 540, 540, 540, 540, 600, 600]
    act_green  = [9.0, 9.0, 9.0, 9.0, 9.0, 10.0, 10.0]
    print("1 all green:", Conditions(pred_green, act_green))

    pred_red = [540, 540, 450, 540, 540, 600, 600]
    act_red  = [9.0, 9.0, 7.0, 9.0, 9.0, 10.0, 10.0]
    print("2 red on both:", Conditions(pred_red, act_red))
"""