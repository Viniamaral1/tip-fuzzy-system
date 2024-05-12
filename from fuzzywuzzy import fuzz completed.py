import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1 Create input variables
service_rate = ctrl.Antecedent(np.arange(0, 11, 0.1), 'service_rate') 

# 2 Create output variable
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# 3 Define membership functions to service rate
service_rate['poor'] = fuzz.trimf(service_rate.universe, [0, 0, 5])
service_rate['average'] = fuzz.trimf(service_rate.universe, [0, 5, 10])
service_rate['excellent'] = fuzz.trimf(service_rate.universe, [5, 10, 10])

# 4 Define membership functions to tip
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

# 5 Define rules
rule1 = ctrl.Rule(service_rate['poor'], tip['low'])
rule2 = ctrl.Rule(service_rate['average'], tip['medium'])
rule3 = ctrl.Rule(service_rate['excellent'], tip['high'])

# 6 Create control system
tip_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tip_calculator = ctrl.ControlSystemSimulation(tip_ctrl)

# 7 Map words to numerical values
rating_mapping = {
    "poor": 2,   
    "average": 5,
    "excellent": 8
}

# 8 Loop to allow rating again
while True:
    # 9 Set input value
    service_rate_input_word = input("Thank you for visit us, please rate the services provided (poor/average/excellent): ").lower()
    
    # 10 Check if input is valid
    if service_rate_input_word not in rating_mapping:
        print("Incorrect rating. Please try again.")
        continue

    # 11 Convert word rating to numerical value
    service_rate_input = rating_mapping[service_rate_input_word]

    # 12 Compute tip
    tip_calculator.input['service_rate'] = service_rate_input
    tip_calculator.compute()

    # 13 Output result
    print("Recommended tip:", tip_calculator.output['tip'])

    # 14 Ask if the user wants to rate again
    choice = input("Do you want to rate again? (yes/no): ").lower()
    if choice != 'yes':
        print("Thank you for rating our services. You rated", service_rate_input_word, "and recommended", tip_calculator.output['tip'], "as tip.")
        break
