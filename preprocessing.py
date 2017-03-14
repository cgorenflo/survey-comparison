import pandas as pd
import math


def map_email_addresses():
    survey1 = pd.read_excel("survey 1.xlsx")
    survey2 = pd.read_excel("survey 2 numerical.xls", header=[0, 1])
    survey3 = pd.read_excel("survey 3 numerical.xls", header=[0, 1])


    set_column_names(survey1, survey2, survey3)
    set_row_labels(survey1)
    set_row_labels(survey2)
    set_row_labels(survey3)
    survey3 = survey3[survey3["email"].notnull()]

    replace_string_values_with_integers(survey1)

    filtered_survey1 = survey1[survey1["email"].isin(survey2["email"])].sort_values("email", ascending=True)
    filtered_survey2 = survey2[survey2["email"].isin(survey1["email"])].sort_values("email", ascending=True)
    filtered_survey3 = survey3[survey3["email"].isin(survey1["email"])].sort_values("email", ascending=True)

    with pd.ExcelWriter("survey1_participants.xlsx") as writer:
        filtered_survey1.to_excel(writer)

    with pd.ExcelWriter("survey2_participants.xlsx") as writer:
        filtered_survey2.to_excel(writer)

    with pd.ExcelWriter("survey3_participants.xlsx") as writer:
        filtered_survey3.to_excel(writer)


def replace_string_values_with_integers(survey1):
    survey1.replace(
        ["very unimportant", "quite unimportant", "somewhat unimportant", "somewhat important", "quite important",
         "very important"], list(range(1, 7)), inplace=True)
    survey1.replace(
        ["(almost) daily", "1-3 days per week", "1-3 days per month", "less than once per month", "(almost) never"],
        list(range(1, 6)), inplace=True)

    survey1.replace(
        ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        list(range(1, 6)), inplace=True)
    survey1.replace("Strongly disagree",1, inplace=True)


def set_row_labels(survey):
    survey.set_index("email", drop=False, inplace=True)


def set_column_names(survey1, survey2, survey3):
    survey1.columns = map(str, range(182))
    survey2.columns = map(str, range(166))
    survey3.columns = map(str, range(166))

    same_columns = {"51": "independence_importance",
                    "52": "stress_importance",
                    "53": "cost_importance",
                    "54": "status_importance",
                    "55": "fun_importance",
                    "56": "environment_importance",
                    "57": "reliability_importance",
                    "58": "comfort_importance",
                    "59": "safety_importance",
                    "60": "health_importance",
                    "61": "independence_cars",
                    "62": "independence_bikes",
                    "63": "independence_ebikes",
                    "64": "independence_transit",
                    "65": "independence_walk",
                    "66": "stress_cars",
                    "67": "stress_bikes",
                    "68": "stress_ebikes",
                    "69": "stress_transit",
                    "70": "stress_walk",
                    "71": "cost_cars",
                    "72": "cost_bikes",
                    "73": "cost_ebikes",
                    "74": "cost_transit",
                    "75": "cost_walk",
                    "76": "status_cars",
                    "77": "status_bikes",
                    "78": "status_ebikes",
                    "79": "status_transit",
                    "80": "status_walk",
                    "81": "fun_cars",
                    "82": "fun_bikes",
                    "83": "fun_ebikes",
                    "84": "fun_transit",
                    "85": "fun_walk",
                    "86": "environment_cars",
                    "87": "environment_bikes",
                    "88": "environment_ebikes",
                    "89": "environment_transit",
                    "90": "environment_walk",
                    "91": "reliability_cars",
                    "92": "reliability_bikes",
                    "93": "reliability_ebikes",
                    "94": "reliability_transit",
                    "95": "reliability_walk",
                    "96": "comfort_cars",
                    "97": "comfort_bikes",
                    "98": "comfort_ebikes",
                    "99": "comfort_transit",
                    "100": "comfort_walk",
                    "101": "safety_cars",
                    "102": "safety_bikes",
                    "103": "safety_ebikes",
                    "104": "safety_transit",
                    "105": "safety_walk",
                    "106": "health_cars",
                    "107": "health_bikes",
                    "108": "health_ebikes",
                    "109": "health_transit",
                    "110": "health_walk"}

    survey1.rename(columns={"172": "email", **same_columns}, inplace=True)
    survey2.rename(columns={"4": "email", **same_columns}, inplace=True)
    survey3.rename(columns={"4": "email", **same_columns}, inplace=True)


map_email_addresses()
