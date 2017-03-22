import matplotlib.pyplot as plt
import numpy
import pandas as pd

import radar_chart

survey1 = pd.read_excel("survey1_participants.xlsx")
survey2 = pd.read_excel("survey2_participants.xlsx")
survey3 = pd.read_excel("survey3_participants.xlsx")

result = survey1.merge(survey2, how='left', on=["email"])
result = result.merge(survey3, how='left', on=["email"])


def plot(figure, subplotargs, column):
    pos = list(range(len(result['email'])))
    width = 0.2

    sub = figure.add_subplot(subplotargs, title=column, xticks=[p + 1.5 * width for p in pos], xticklabels=result.index,
                             xlim=[min(pos) - width, max(pos) + width * 4],
                             ylim=[0, 0.4 + max(max(result[column]), max(result[column + '_x']),
                                                max(result[column + '_y']))])

    # Create a bar with pre_score data,
    # in position pos,
    sub.bar(pos,
            # using df['pre_score'] data,
            result[column],
            # of width
            width,
            # with alpha 0.5
            alpha=0.6,
            # with color
            color='black')
    sub.plot(pos, [numpy.mean(result[column])] * len(pos), 'k--')

    # Create a bar with mid_score data,
    # in position pos + some width buffer,
    plt.bar([p + width for p in pos],
            # using df['mid_score'] data,
            result[column + '_x'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.6,
            # with color
            color='red')
    sub.plot(pos, [numpy.mean(result[column + '_x'])] * len(pos), 'r--')

    # Create a bar with post_score data,
    # in position pos + some width buffer,
    plt.bar([p + width * 2 for p in pos],
            # using df['post_score'] data,
            result[column + '_y'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.6,
            # with color
            color='blue')
    sub.plot(pos, [numpy.mean(result[column + '_y'])] * len(pos), 'b--')


figrad = plt.figure()
radar = radar_chart.ComplexRadar(figrad, ["independence_importance",
                         "stress_importance",
                         "cost_importance",
                         "status_importance",
                         "fun_importance",
                         "environment_importance"],[(0,7)]*6)

participant_index = 1
radar.plot(tuple(result[["independence_importance",
                         "stress_importance",
                         "cost_importance",
                         "status_importance",
                         "fun_importance",
                         "environment_importance"]].iloc[participant_index]))
radar.fill(tuple(result[["independence_importance",
                         "stress_importance",
                         "cost_importance",
                         "status_importance",
                         "fun_importance",
                         "environment_importance"]].iloc[participant_index]), alpha=0.2)

radar.plot(tuple(result[["independence_importance_x",
                         "stress_importance_x",
                         "cost_importance_x",
                         "status_importance_x",
                         "fun_importance_x",
                         "environment_importance_x"]].iloc[participant_index]))
radar.fill(tuple(result[["independence_importance_x",
                         "stress_importance_x",
                         "cost_importance_x",
                         "status_importance_x",
                         "fun_importance_x",
                         "environment_importance_x"]].iloc[participant_index]), alpha=0.2)

radar.plot(tuple(result[["independence_importance_y",
                         "stress_importance_y",
                         "cost_importance_y",
                         "status_importance_y",
                         "fun_importance_y",
                         "environment_importance_y"]].iloc[participant_index]))
radar.fill(tuple(result[["independence_importance_y",
                         "stress_importance_y",
                         "cost_importance_y",
                         "status_importance_y",
                         "fun_importance_y",
                         "environment_importance_y"]].iloc[participant_index]), alpha=0.2)
plt.savefig("radar.png")


fig1a = plt.figure()
plot(fig1a, 321, "independence_importance")
plot(fig1a, 322, "stress_importance")
plot(fig1a, 323, "cost_importance")
plot(fig1a, 324, "status_importance")
plot(fig1a, 325, "fun_importance")
plot(fig1a, 326, "environment_importance")
plt.savefig("importance1.png")

fig1b = plt.figure()
plot(fig1b, 321, "reliability_importance")
plot(fig1b, 322, "comfort_importance")
plot(fig1b, 323, "safety_importance")
plot(fig1b, 324, "health_importance")
plt.savefig("importance2.png")
#
# fig2 = plt.figure()
# plot(fig2, 321, "independence_cars")
# plot(fig2, 322, "independence_bikes")
# plot(fig2, 323, "independence_ebikes")
# plot(fig2, 324, "independence_transit")
# plot(fig2, 325, "independence_walk")
# plt.savefig("independence.png")
#
# fig3 = plt.figure()
# plot(fig3, 321, "stress_cars")
# plot(fig3, 322, "stress_bikes")
# plot(fig3, 323, "stress_ebikes")
# plot(fig3, 324, "stress_transit")
# plot(fig3, 325, "stress_walk")
# plt.savefig("stress.png")
#
# fig4 = plt.figure()
# plot(fig4, 321, "cost_cars")
# plot(fig4, 322, "cost_bikes")
# plot(fig4, 323, "cost_ebikes")
# plot(fig4, 324, "cost_transit")
# plot(fig4, 325, "cost_walk")
# plt.savefig("cost.png")
#
# fig5 = plt.figure()
# plot(fig5, 321, "status_cars")
# plot(fig5, 322, "status_bikes")
# plot(fig5, 323, "status_ebikes")
# plot(fig5, 324, "status_transit")
# plot(fig5, 325, "status_walk")
# plt.savefig("status.png")
#
# fig6 = plt.figure()
# plot(fig6, 321, "fun_cars")
# plot(fig6, 322, "fun_bikes")
# plot(fig6, 323, "fun_ebikes")
# plot(fig6, 324, "fun_transit")
# plot(fig6, 325, "fun_walk")
# plt.savefig("fun.png")
#
# fig7 = plt.figure()
# plot(fig7, 321, "environment_cars")
# plot(fig7, 322, "environment_bikes")
# plot(fig7, 323, "environment_ebikes")
# plot(fig7, 324, "environment_transit")
# plot(fig7, 325, "environment_walk")
# plt.savefig("environment.png")
#
# fig8 = plt.figure()
# plot(fig8, 321, "reliability_cars")
# plot(fig8, 322, "reliability_bikes")
# plot(fig8, 323, "reliability_ebikes")
# plot(fig8, 324, "reliability_transit")
# plot(fig8, 325, "reliability_walk")
# plt.savefig("reliability.png")
#
# fig9 = plt.figure()
# plot(fig9, 321, "comfort_cars")
# plot(fig9, 322, "comfort_bikes")
# plot(fig9, 323, "comfort_ebikes")
# plot(fig9, 324, "comfort_transit")
# plot(fig9, 325, "comfort_walk")
# plt.savefig("comfort.png")
#
# fig10 = plt.figure()
# plot(fig10, 321, "safety_cars")
# plot(fig10, 322, "safety_bikes")
# plot(fig10, 323, "safety_ebikes")
# plot(fig10, 324, "safety_transit")
# plot(fig10, 325, "safety_walk")
# plt.savefig("safety.png")
#
# fig11 = plt.figure()
# plot(fig11, 321, "health_cars")
# plot(fig11, 322, "health_bikes")
# plot(fig11, 323, "health_ebikes")
# plot(fig11, 324, "health_transit")
# plot(fig11, 325, "health_walk")
plt.savefig("radar.png")

plt.show()
