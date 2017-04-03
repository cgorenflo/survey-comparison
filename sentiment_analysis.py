import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy
import pandas as pd

# import radar_chart

survey1 = pd.read_excel("survey1_participants.xlsx")
survey2 = pd.read_excel("survey2_participants.xlsx")
survey3 = pd.read_excel("survey3_participants.xlsx")

result = survey1.merge(survey2, how='left', on=["email"])
result = result.merge(survey3, how='left', on=["email"])

figsize = (10, 5)
dpi = 600


def plot(column,title):
    plt.figure(figsize=figsize, dpi=dpi)
    pos = list(range(len(result['email'])))
    width = 0.2
    plt.title(title)
    plt.xticks([p + 1.5 * width for p in pos], [""]*len(pos))
    plt.xlim([min(pos) - width, max(pos) + width * 4])
    plt.ylim([0, 9])
    plt.xlabel("participants")
    plt.yticks(range(1, 7), [
        "very unimportant",
        "quite unimportant",
        "somewhat unimportant",
        "somewhat important",
        "quite important",
        "very important"
    ])
    plt.tight_layout()

    # Create a bar with pre_score data,
    # in position pos,
    s1= plt.bar(pos,
            # using df['pre_score'] data,
            result[column],
            # of width
            width,
            # with alpha 0.5
            alpha=1,
            # with color
            color='royalblue')
    plt.plot([min(pos) - width, max(pos) + width * 4], [numpy.mean(result[column])] * 2, '--', color="royalblue")

    # Create a bar with mid_score data,
    # in position pos + some width buffer,
    s2 = plt.bar([p + width for p in pos],
            # using df['mid_score'] data,
            result[column + '_x'],
            # of width
            width,
            # with alpha 0.5
            alpha=1,
            # with color
            color='darkorange')
    plt.plot([min(pos) - width, max(pos) + width * 4], [numpy.mean(result[column + '_x'])] * 2, '--',
             color="darkorange")

    # Create a bar with post_score data,
    # in position pos + some width buffer,
    s3 = plt.bar([p + width * 2 for p in pos],
            # using df['post_score'] data,
            result[column + '_y'],
            # of width
            width,
            # with alpha 0.5
            alpha=1,
            # with color
            color='black')
    plt.plot([min(pos) - width, max(pos) + width * 4], [numpy.mean(result[column + '_y'])] * 2, '--', color="black")
    plt.legend([s1, s2, s3], ["survey 1", "survey 2", "survey 3"])
    plt.savefig("survey_{column}.png".format(column=column))


plot("independence_importance","independence")

plot("stress_importance", "stress-free travel")
plot("cost_importance", "cost")
plot("status_importance", "social status")
plot("fun_importance", "fun")
plot("environment_importance", "eco-friendliness")

plot("reliability_importance", "reliability")
plot("comfort_importance","comfort")
plot("safety_importance", "safety")
plot("health_importance","healthiness")

props = ["independence", "stress", "cost", "status", "fun", "environment", "reliability", "comfort", "safety",
         "health"]

propslabels = ["independence", "stress-free travel", "low cost", "fits social status", "fun", "eco-friendliness", "reliability",
               "comfort", "safety", "healthiness"]
modes = ["_cars", "_bikes", "_ebikes", "_transit", "_walk"]


def plot_mean(columns):
    plt.figure(figsize=figsize, dpi=dpi)
    plt.xticks([p + 1.5 * width for p in pos], propslabels, rotation=30, ha="center")
    plt.yticks(range(1, 6), ["Strongly Disagree",
                             "Disagree",
                             "Neutral",
                             "Agree",
                             "Strongly Agree"
                             ])
    plt.xlim([min(pos) - width, max(pos) + width * 4])
    plt.ylim([0, 7])
    plt.tight_layout()
    s1 = plt.bar(pos,
                 [numpy.mean(result[c]) for c in columns],
                 width,
                 alpha=1,
                 color="royalblue"
                 )
    plt.errorbar([p + 0.5 * width for p in pos],
                 [numpy.mean(result[c]) for c in columns],
                 [numpy.std(result[c]) for c in columns],
                 alpha=1,
                 linestyle='None',
                 color='red')
    s2 = plt.bar([p + width for p in pos],
                 [numpy.mean(result[c + '_x']) for c in columns],
                 width,
                 alpha=1,
                 color="darkorange")
    plt.errorbar([p + 1.5 * width for p in pos],
                 [numpy.mean(result[c + '_x']) for c in columns],
                 [numpy.std(result[c + '_x']) for c in columns],
                 alpha=1,
                 linestyle='None',
                 color='red')
    s3 = plt.bar([p + width * 2 for p in pos],
                 [numpy.mean(result[c + '_y']) for c in columns],
                 width,
                 alpha=1,
                 color='black')
    plt.errorbar([p + width * 2.5 for p in pos],
                 [numpy.mean(result[c + '_y']) for c in columns],
                 [numpy.std(result[c + '_y']) for c in columns],
                 alpha=1,
                 linestyle='None',
                 color='red')

    plt.legend([s1, s2, s3], ["survey 1", "survey 2", "survey 3"])


pos = list(range(len(props)))
width = 0.2

for m in modes:
    columns = [p + m for p in props]
    plot_mean(columns)
    plt.savefig("survey{modes}.png".format(modes=m))
plt.show()
