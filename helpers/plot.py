import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.legend_handler import HandlerLine2D


def plot(csv_file, delimit='\t', data_cols=(0, 2, 3, 4), plot_title="", output_file = "plot.png"):
    """
    The file to plot. Expected file format
    N	Test file name	Micro Precision	Micro Recall	Micro F1	Macro Precision	Macro Recall	Macro F1
    1	Test With Gnorm 	0.156	0.4591	0.2329	0.2111	0.4551	0.2495
    2	Test With Gnorm 	0.2977	0.359	0.3255	0.2752	0.3771	0.2901
    3	Test With Gnorm 	0.4	0.3084	0.3483	0.2868	0.3353	0.289
    ....
    :param plot_title: The plot title
    :param data_cols: The data col numbers
    :param csv_file:

    :param delimit:
    """

    # Load file
    data = np.loadtxt(csv_file, delimiter=delimit, skiprows=1, usecols=data_cols)

    # Set up data
    n = data[:, 0]
    prec = data[:, 1]
    recall = data[:, 2]
    fscore = data[:, 3]

    # configure plot
    plt.xlabel('Threshold N (Number of sentences containing gene pairs)')
    plt.ylabel('Score')
    axes = plt.gca()
    axes.set_ylim([0, 1.2])
    axes.yaxis.set_ticks(np.arange(0, 1.2, .1))

    l_prec, = plt.plot(n, prec, 'r--', label='Precision')
    l_recall, = plt.plot(n, recall, 'b--', label='Recall')
    l_fscore, = plt.plot(n, fscore, 'g--', label='F-Score')

    plt.title(plot_title)

    plt.legend(handler_map={l_prec: HandlerLine2D(numpoints=4)})

    plt.savefig(output_file, dpi=300)

    plt.close()


plot(os.path.join(os.path.dirname(__file__), 'Data_Test_GNorm_N_Vs_FScore.txt'),
     plot_title="Test data using GNormPlus entity annotation", output_file = "CoOccurance_N_Vs_Score_Gnorm.png")
plot(os.path.join(os.path.dirname(__file__), 'Data_Test_GNormMerge_N_Vs_FScore.txt'),
     plot_title="Test data using GNormPlus and Task entity annotation", output_file = "CoOccurance_N_Vs_Score_Gnorm_Task.png")
