import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

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
    # print("sdsdsd", dir(tipping_ctrl.antecedents), list(tipping_ctrl.antecedents))
    # print(tipping_ctrl.graph.nodes())

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
    tipping.input["quality"] = l
    tipping.input["service"] = p

    # Crunch the numbers
    tipping.compute()
    # print(tipping._get_inputs())

    print("Time amount = ", tipping.output["tip"])
    # tip.view(sim=tipping)

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    ax0.plot(quality.universe, quality["poor"].mf, "b", linewidth=1.5, label="Low")
    ax0.plot(quality.universe, quality["medium"].mf, "g", linewidth=1.5, label="Medium")
    ax0.plot(quality.universe, quality["high"].mf, "r", linewidth=1.5, label="High")
    ax0.set_title("Loading")
    ax0.legend()

    ax1.plot(
        service.universe,
        service["acceptable"].mf,
        "b",
        linewidth=1.5,
        label="Acceptable",
    )
    ax1.plot(
        service.universe,
        service["unacceptable"].mf,
        "g",
        linewidth=1.5,
        label="Unacceptable",
    )

    ax1.set_title("Packet Loss Rate")
    ax1.legend()

    ax2.plot(tip.universe, tip["low"].mf, "b", linewidth=1.5, label="low")
    ax2.plot(tip.universe, tip["medium"].mf, "g", linewidth=1.5, label="medium")
    ax2.plot(tip.universe, tip["high"].mf, "r", linewidth=1.5, label="high")
    ax2.set_title("Time amount")
    ax2.legend()

    # ax3.plot(tip.universe, tip["low"].mf, "b", linewidth=0.5, linestyle="--")
    # ax3.plot(tip.universe, tip["medium"].mf, "g", linewidth=0.5, linestyle="--")
    # ax3.plot(tip.universe, tip["high"], "r", linewidth=0.5, linestyle="--")
    # ax3.fill_between(tip, tip0, aggregated, facecolor="Orange", alpha=0.7)
    # ax3.plot([tip, tip], [0, tip_activation], "k", linewidth=1.5, alpha=0.9)

    # ax3.set_title("Aggregated membership and result (line)")
    # ax3.legend()
    # Turn off top/right axes
    for ax in (ax0, ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    # plt.tight_layout()
    plt.savefig("out2.png")

    # plt.show()
    return tipping.output["tip"]
