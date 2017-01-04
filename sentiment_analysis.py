import pandas as pd
import matplotlib.pyplot as plt

survey1 = pd.read_excel("survey1_participants.xlsx")
survey2 = pd.read_excel("survey2_participants.xlsx")


def plot(figure, subplotargs, column):
    sdiff = (survey2[column] - survey1[column]).sort_values()
    s1 = survey1.reindex(sdiff.index, copy=True)
    s2 = survey2.reindex(sdiff.index, copy=True)

    sub = figure.add_subplot(subplotargs, title=column, xticks=range(len(s1)), xticklabels=s1.index, xlim=[-1, len(s1)],
                             ylim=[-7, 7])
    sub.plot(s1[column].values, 'ro')
    sub.plot(s2[column].values, 'bo')
    sub.bar([i - 0.5 for i in range(len(sdiff))], sdiff.values, color='g')


fig1a = plt.figure()
plot(fig1a, 231, "independence_importance")
plot(fig1a, 232, "stress_importance")
plot(fig1a, 233, "cost_importance")
plot(fig1a, 234, "status_importance")
plot(fig1a, 235, "fun_importance")
plot(fig1a, 236, "environment_importance")

fig1b = plt.figure()
plot(fig1b, 231, "reliability_importance")
plot(fig1b, 232, "comfort_importance")
plot(fig1b, 233, "safety_importance")
plot(fig1b, 234, "health_importance")

fig2 = plt.figure()
plot(fig2, 231, "independence_cars")
plot(fig2, 232, "independence_bikes")
plot(fig2, 233, "independence_ebikes")
plot(fig2, 234, "independence_transit")
plot(fig2, 235, "independence_walk")

fig3 = plt.figure()
plot(fig3, 231,"stress_cars")
plot(fig3, 232,"stress_bikes")
plot(fig3, 233,"stress_ebikes")
plot(fig3, 234,"stress_transit")
plot(fig3, 235,"stress_walk")

fig4 = plt.figure()
plot(fig4, 231,"cost_cars")
plot(fig4, 232,"cost_bikes")
plot(fig4, 233,"cost_ebikes")
plot(fig4, 234,"cost_transit")
plot(fig4, 235,"cost_walk")

fig5 = plt.figure()
plot(fig5, 231,"status_cars")
plot(fig5, 232,"status_bikes")
plot(fig5, 233,"status_ebikes")
plot(fig5, 234,"status_transit")
plot(fig5, 235,"status_walk")

fig6 = plt.figure()
plot(fig6, 231,"fun_cars")
plot(fig6, 232,"fun_bikes")
plot(fig6, 233,"fun_ebikes")
plot(fig6, 234,"fun_transit")
plot(fig6, 235,"fun_walk")

fig7 = plt.figure()
plot(fig7, 231,"environment_cars")
plot(fig7, 232,"environment_bikes")
plot(fig7, 233,"environment_ebikes")
plot(fig7, 234,"environment_transit")
plot(fig7, 235,"environment_walk")

fig8 = plt.figure()
plot(fig8, 231,"reliability_cars")
plot(fig8, 232,"reliability_bikes")
plot(fig8, 233,"reliability_ebikes")
plot(fig8, 234,"reliability_transit")
plot(fig8, 235,"reliability_walk")

fig9 = plt.figure()
plot(fig9, 231,"comfort_cars")
plot(fig9, 232,"comfort_bikes")
plot(fig9, 233,"comfort_ebikes")
plot(fig9, 234,"comfort_transit")
plot(fig9, 235,"comfort_walk")

fig10 = plt.figure()
plot(fig10, 231,"safety_cars")
plot(fig10, 232,"safety_bikes")
plot(fig10, 233,"safety_ebikes")
plot(fig10, 234,"safety_transit")
plot(fig10, 235,"safety_walk")

fig11 = plt.figure()
plot(fig11, 231,"health_cars")
plot(fig11, 232,"health_bikes")
plot(fig11, 233,"health_ebikes")
plot(fig11, 234,"health_transit")
plot(fig11, 235,"health_walk")

plt.show()
