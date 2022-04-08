import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control.visualization import FuzzyVariableVisualizer
import matplotlib.pyplot as plt
from django.conf import settings
import random

# New Antecedent/Consequent objects hold universe variables and membership
# functions


def calculate(l, p):
    quality = ctrl.Antecedent(np.arange(0, 1.1, 0.1), "quality")
    service = ctrl.Antecedent(np.arange(pow(10, -10), 0.1, 0.0079), "service")
    tip = ctrl.Consequent(np.arange(0, 61, 1), "tip")

    quality["poor"] = fuzz.zmf(quality.universe, 0, 0.15)
    quality["medium"] = fuzz.trimf(quality.universe, [0.15, 0.5, 0.85])
    quality["high"] = fuzz.smf(quality.universe, 0.5, 0.85)

    service["acceptable"] = fuzz.zmf(service.universe, pow(10, -10), pow(10, -6))
    service["unacceptable"] = fuzz.smf(service.universe, pow(10, -6), pow(10, -5))
    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    tip["low"] = fuzz.zmf(tip.universe, 5, 10)
    tip["medium"] = fuzz.trimf(tip.universe, [20, 30, 40])
    tip["high"] = fuzz.smf(tip.universe, 40, 50)

    rule1 = ctrl.Rule(quality["poor"] & service["acceptable"], tip["high"])
    rule2 = ctrl.Rule(quality["poor"] & service["unacceptable"], tip["low"])
    rule3 = ctrl.Rule(quality["medium"] & service["acceptable"], tip["medium"])
    rule4 = ctrl.Rule(quality["medium"] & service["unacceptable"], tip["low"])
    rule5 = ctrl.Rule(quality["high"] & service["acceptable"], tip["medium"])
    rule6 = ctrl.Rule(quality["high"] & service["unacceptable"], tip["low"])

    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
    tipping.input["quality"] = l
    tipping.input["service"] = p

    # Crunch the numbers
    tipping.compute()

    # print("Time amount = ", tipping.output["tip"])
    # tip.view(sim=tipping)
    result, ax = FuzzyVariableVisualizer(tip).view(sim=tipping)
    random_image_name = f"result_{random.randint(1,99999)}"
    result.savefig(f"{settings.BASE_DIR}\\app\static\\app\\{random_image_name}.png")

    # fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    # ax0.plot(quality.universe, quality["poor"].mf, "b", linewidth=1.5, label="Low")
    # ax0.plot(quality.universe, quality["medium"].mf, "g", linewidth=1.5, label="Medium")
    # ax0.plot(quality.universe, quality["high"].mf, "r", linewidth=1.5, label="High")
    # ax0.set_title("Loading")
    # ax0.legend()

    # ax1.plot(
    #     service.universe,
    #     service["acceptable"].mf,
    #     "b",
    #     linewidth=1.5,
    #     label="Acceptable",
    # )
    # ax1.plot(
    #     service.universe,
    #     service["unacceptable"].mf,
    #     "g",
    #     linewidth=1.5,
    #     label="Unacceptable",
    # )

    # ax1.set_title("Packet Loss Rate")
    # ax1.legend()

    # ax2.plot(tip.universe, tip["low"].mf, "b", linewidth=1.5, label="low")
    # ax2.plot(tip.universe, tip["medium"].mf, "g", linewidth=1.5, label="medium")
    # ax2.plot(tip.universe, tip["high"].mf, "r", linewidth=1.5, label="high")
    # ax2.set_title("Time amount")
    # ax2.legend()

    # for ax in (ax0, ax1, ax2):
    #     ax.spines["top"].set_visible(False)
    #     ax.spines["right"].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()

    # plt.tight_layout()
    # plt.savefig(f"{settings.BASE_DIR}\\app\static\\app\output.png")

    # plt.show()
    return tipping.output["tip"], random_image_name


# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html
