"""
=========================================
Activity regrouping schemes to be used with PAAWS.
=========================================
Author: Veronika K. Potter
Email: potter[dot]v[at]northeastern[dot]edu (potter.v@northeastern.edu)
"""

# The mapping schemes used across our experiments.
MAPPING_SCHEMES = {
    # Mapping with 5 activities, can be used with SimFL+Lab or FL data.
    "lab_fl_5": {
        "Sitting_Still": "Sitting",
        "Sitting_With_Movement": "Sitting",
        "Sit_Recline_Talk_Lab": "Sitting",
        "Sit_Recline_Web_Browse_Lab": "Sitting",
        "Sit_Writing_Lab": "Sitting",
        "Sit_Typing_Lab": "Sitting",

        "Standing_Still": "Standing",
        "Standing_With_Movement": "Standing",
        "Stand_Conversation_Lab": "Standing",

        "Lying_Still": "Lying_Down",
        "Lying_With_Movement": "Lying_Down",
        "Lying_On_Back_Lab": "Lying_Down",
        "Lying_On_Right_Side_Lab": "Lying_Down",
        "Lying_On_Stomach_Lab": "Lying_Down",
        "Lying_On_Left_Side_Lab": "Lying_Down",

        "Walking": "Walking",
        "Treadmill_2mph_Lab": "Walking",
        "Treadmill_3mph_Conversation_Lab": "Walking",
        "Treadmill_3mph_Free_Walk_Lab": "Walking",
        "Treadmill_3mph_Drink_Lab": "Walking",
        "Treadmill_3mph_Briefcase_Lab": "Walking",
        "Treadmill_3mph_Phone_Lab": "Walking",
        "Treadmill_3mph_Hands_Pockets_Lab": "Walking",
        "Walking_Fast": "Walking",
        "Walking_Slow": "Walking",

        'Stationary_Biking_300_Lab': 'Biking',
        'Exercising_Gym_Stationary_Bicycle': 'Biking',
        'Cycling_Active_Pedaling_Stationary_Bicycle': 'Biking',
        'Cycling_Active_Pedaling_Regular_Bicycle': 'Biking',
    },

    # Mapping with 9 activities, can be used with SimFL+Lab or FL data.
    "lab_fl_9": {
        "Sitting_Still": "Sitting",
        "Sitting_With_Movement": "Sitting",
        "Sit_Recline_Talk_Lab": "Sitting",
        "Sit_Recline_Web_Browse_Lab": "Sitting",
        "Sit_Writing_Lab": "Sitting",
        "Sit_Typing_Lab": "Sitting",

        "Standing_Still": "Standing",
        "Standing_With_Movement": "Standing",
        "Stand_Conversation_Lab": "Standing",

        "Lying_Still": "Lying_Down",
        "Lying_With_Movement": "Lying_Down",
        "Lying_On_Back_Lab": "Lying_Down",
        "Lying_On_Right_Side_Lab": "Lying_Down",
        "Lying_On_Stomach_Lab": "Lying_Down",
        "Lying_On_Left_Side_Lab": "Lying_Down",

        "Walking": "Walking",
        "Treadmill_2mph_Lab": "Walking",
        "Treadmill_3mph_Conversation_Lab": "Walking",
        "Treadmill_3mph_Free_Walk_Lab": "Walking",
        "Treadmill_3mph_Drink_Lab": "Walking",
        "Treadmill_3mph_Briefcase_Lab": "Walking",
        "Treadmill_3mph_Phone_Lab": "Walking",
        "Treadmill_3mph_Hands_Pockets_Lab": "Walking",
        "Walking_Fast": "Walking",
        "Walking_Slow": "Walking",

        "Walking_Up_Stairs": "Walking_Up_Stairs",

        "Walking_Down_Stairs": "Walking_Down_Stairs",

        "Ab_Crunches_Lab": "Gym_Exercises",
        "Arm_Curls_Lab": "Gym_Exercises",
        "Push_Up_Lab": "Gym_Exercises",
        "Push_Up_Modified_Lab": "Gym_Exercises",
        "Machine_Leg_Press_Lab": "Gym_Exercises",
        "Machine_Chest_Press_Lab": "Gym_Exercises",
        "Treadmill_5.5mph_Lab": "Gym_Exercises",

        "Cycling_Active_Pedaling_Regular_Bicycle": "Biking",
        "Stationary_Biking_300_Lab": "Biking",

        'Organizing_Shelf/Closet': 'Household_Chores',
        'Sweeping': 'Household_Chores',
        'Vacuuming': 'Household_Chores',
        'Stand_Shelf_Load_Lab': 'Household_Chores',
        'Stand_Shelf_Unload_Lab': 'Household_Chores',
        'Washing_Dishes_Lab': 'Household_Chores',
        'Chopping_Food_Lab': 'Household_Chores'
    },

    # Mapping with 42 activities, used with SimFL+Lab data only.
    "lab_42": {
        "Ab_Crunches_Lab": "Ab_Crunches_Lab",
        "Arm_Curls_Lab": "Arm_Curls_Lab",
        "Chopping_Food_Lab": "Chopping_Food_Lab",
        "Cycling_Active_Pedaling_Regular_Bicycle":
            "Cycling_Active_Pedaling_Regular_Bicycle",
        "Folding_Clothes": "Folding_Clothes",
        "Lying_On_Back_Lab": "Lying_On_Back_Lab",
        "Lying_On_Left_Side_Lab": "Lying_On_Left_Side_Lab",
        "Lying_On_Right_Side_Lab": "Lying_On_Right_Side_Lab",
        "Lying_On_Stomach_Lab": "Lying_On_Stomach_Lab",
        "Machine_Chest_Press_Lab": "Machine_Chest_Press_Lab",
        "Machine_Leg_Press_Lab": "Machine_Leg_Press_Lab",
        "Organizing_Shelf/Cabinet": "Organizing_Shelf/Cabinet",
        "Playing_Frisbee": "Playing_Frisbee",
        "Push_Up_Lab": "Push_Up_Lab",
        "Push_Up_Modified_Lab": "Push_Up_Modified_Lab",
        "Sit_Recline_Talk_Lab": "Sit_Recline_Talk_Lab",
        "Sit_Recline_Web_Browse_Lab": "Sit_Recline_Web_Browse_Lab",
        "Sit_Typing_Lab": "Sit_Typing_Lab",
        "Sit_Writing_Lab": "Sit_Writing_Lab",
        "Sitting_Still": "Sitting_Still",
        "Sitting_With_Movement": "Sitting_With_Movement",
        "Stand_Conversation_Lab": "Stand_Conversation_Lab",
        "Stand_Shelf_Load_Lab": "Stand_Shelf_Load_Lab",
        "Stand_Shelf_Unload_Lab": "Stand_Shelf_Unload_Lab",
        "Standing_Still": "Standing_Still",
        "Standing_With_Movement": "Standing_With_Movement",
        "Stationary_Biking_300_Lab": "Stationary_Biking_300_Lab",
        "Sweeping": "Sweeping",
        "Treadmill_2mph_Lab": "Treadmill_2mph_Lab",
        "Treadmill_3mph_Conversation_Lab": "Treadmill_3mph_Conversation_Lab",
        "Treadmill_3mph_Drink_Lab": "Treadmill_3mph_Drink_Lab",
        "Treadmill_3mph_Free_Walk_Lab": "Treadmill_3mph_Free_Walk_Lab",
        "Treadmill_3mph_Hands_Pockets_Lab": "Treadmill_3mph_Hands_Pockets_Lab",
        "Treadmill_3mph_Briefcase_Lab": "Treadmill_3mph_Briefcase_Lab",
        "Treadmill_3mph_Phone_Lab": "Treadmill_3mph_Phone_Lab",
        "Treadmill_4mph_Lab": "Treadmill_4mph_Lab",
        "Treadmill_5.5mph_Lab": "Treadmill_5.5mph_Lab",
        "Vacuuming": "Vacuuming",
        "Walking": "Walking",
        "Walking_Down_Stairs": "Walking_Down_Stairs",
        "Walking_Up_Stairs": "Walking_Up_Stairs",
        "Washing_Dishes_Lab": "Washing_Dishes_Lab",
    },

    # Mapping with 11 activities, used for FL data only.
    "fl_11": {
        'Standing_Still': 'Standing',
        'Stand_Conversation_Lab': 'Standing',
        'Standing_With_Movement': 'Standing',

        'Sitting_Still': 'Sitting',
        'Sit_Typing_Lab': 'Sitting',
        'Sit_Recline_Web_Browse_Lab': 'Sitting',
        'Sit_Writing_Lab': 'Sitting',
        'Sit_Recline_Talk_Lab': 'Sitting',
        'Sitting_With_Movement': 'Sitting',

        'Lying_Still': 'Lying_Down',
        'Lying_On_Left_Side_Lab': 'Lying_Down',
        'Lying_On_Right_Side_Lab': 'Lying_Down',
        'Lying_On_Back_Lab': 'Lying_Down',
        'Lying_On_Stomach_Lab': 'Lying_Down',
        'Lying_With_Movement': 'Lying_Down',

        'Walking': 'Walking',
        'Walking_Slow': 'Walking',
        'Walking_Fast': 'Walking',
        'Walking_Up_Stairs': 'Walking',
        'Walking_Down_Stairs': 'Walking',
        'Walking_Treadmill': 'Walking',
        'Treadmill_2mph_Lab': 'Walking',
        'Treadmill_3mph_Conversation_Lab': 'Walking',
        'Treadmill_3mph_Drink_Lab': 'Walking',
        'Treadmill_3mph_Free_Walk_Lab': 'Walking',
        'Treadmill_3mph_Briefcase_Lab': 'Walking',
        'Treadmill_3mph_Hands_Pockets_Lab': 'Walking',
        'Treadmill_4mph_Lab': 'Walking',

        'Stationary_Biking_300_Lab': 'Biking',
        'Exercising_Gym_Stationary_Bicycle': 'Biking',
        'Cycling_Active_Pedaling_Stationary_Bicycle': 'Biking',
        'Cycling_Active_Pedaling_Regular_Bicycle': 'Biking',

        'In_Transit_Driving_Car': 'Driving',

        'Playing_Frisbee': 'Exercising',
        'Playing_Exergame': 'Exercising',
        'Playing_Sports/Games': 'Exercising',
        'Doing_Resistance_Training_Free_Weights': 'Exercising',
        'Exercising_Gym_Other': 'Exercising',
        'Doing_Resistance_Training_Other': 'Exercising',
        'Exercising_Gym_Treadmill': 'Exercising',
        'Arm_Curls_Lab': 'Exercising',
        'Doing_Martial_Arts': 'Exercising',
        'Push_Up_Modified_Lab': 'Exercising',
        'Doing_Resistance_Training': 'Exercising',
        'Push_Up_Lab': 'Exercising',
        'Ab_Crunches_Lab': 'Exercising',
        'Machine_Leg_Press_Lab': 'Exercising',
        'Machine_Chest_Press_Lab': 'Exercising',
        'Running_Non_Treadmill': 'Exercising',
        'Running_Treadmill': 'Exercising',

        'Dry_Mopping': 'Household_Chores',
        'Cleaning': 'Household_Chores',
        'Dusting': 'Household_Chores',
        'Doing_Common_Housework_Light': 'Household_Chores',
        'Folding_Clothes': 'Household_Chores',
        'Doing_Common_Housework': 'Household_Chores',
        'Ironing': 'Household_Chores',
        'Doing_Dishes': 'Household_Chores',
        'Loading/Unloading_Washing_Machine/Dryer': 'Household_Chores',
        'Doing_Home_Repair_Light': 'Household_Chores',
        'Organizing_Shelf/Closet': 'Household_Chores',
        'Doing_Home_Repair': 'Household_Chores',
        'Putting_Clothes_Away': 'Household_Chores',
        'Packing/Unpacking_Something': 'Household_Chores',
        'Sweeping': 'Household_Chores',
        'Vacuuming': 'Household_Chores',
        'Stand_Shelf_Load_Lab': 'Household_Chores',
        'Stand_Shelf_Unload_Lab': 'Household_Chores',
        'Washing_Dishes_Lab': 'Household_Chores',

        'Chopping_Food_Lab': 'Cooking',
        'Cooking/Prepping_Food': 'Cooking',

        'Eating/Dining': 'Eating/Drinking',

        'Washing_Hands': 'Grooming',
        'Brushing_Teeth': 'Grooming',
        'Brushing/Combing/Tying_Hair': 'Grooming',
        'Washing_Face': 'Grooming',
        'Applying_Makeup': 'Grooming',
        'Flossing_Teeth': 'Grooming',
        'Blowdrying_Hair': 'Grooming',
    },

    # Mapping with 5 sleep stages, used for Sleep data only.
    "sleep_5": {
        "Wake": "Wake",
        "N1": "N1",
        "N2": "N2",
        "N3": "N3",
        "REM": "REM",
    },

    # Mapping with 2 classes (sleep vs. wake), used for Sleep data only.
    "sleep_2": {
        "Wake": "Wake",

        "N1": "Sleep",
        "N2": "Sleep",
        "N3": "Sleep",
        "REM": "Sleep",
    },
}
