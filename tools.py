from typing import Any
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import DataFrame
import pandas as pd

class MakerPlots:
    def __init__(self, data : DataFrame) -> None:
        self.data = data
        sns.set_theme()
        self.all_plots_funs = [
            self.make_corners_hist_plot,
            self.make_boxplots_plot,
            self.make_hists_plot,
            self.make_heatmap_plot,
            self.make_map_plot
        ]

    def make_corners_hist_plot(self):
        bins = 4
        cols = ['rb_corners', 'gt_corners']
        sns.set_theme()
        fig, ax = plt.subplots()
        ax.hist(self.data[cols], bins=bins, label=cols, color=['r', 'b'])
        fig.legend()
        return fig

    def make_boxplots_plot(self):
        fig, axs = plt.subplots(ncols=3)
        fig.set_size_inches(12, 9)
        for data, ax in zip([self.data.iloc[:, 3:6], self.data.iloc[:, 6:9], self.data.iloc[:, 9:]], axs):
            sns.boxplot(data, ax=ax)
        return fig
    
    def make_hists_plot(self):
        bins=range(1, 200, 10)
        fig, axs = plt.subplots(ncols=3)
        fig.set_size_inches(12, 8)
        cols = ['mean', 'floor_mean', 'ceiling_mean']
        for i, cols in enumerate(list(zip(self.data.columns[3:], 
                                          self.data.columns[6:], 
                                          self.data.columns[9:]))):
            for col in cols:
                sns.distplot(self.data[col], bins=bins, ax=axs[i], kde=False)
            axs[i].legend(labels = cols)
        return fig
    
    def make_heatmap_plot(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        sns.heatmap(self.data.iloc[:, 1:].corr().round(3), annot=True, ax=ax)
        return fig

    def make_map_plot(self):
        g = sns.PairGrid(self.data.iloc[:, 3:])
        g.map_upper(sns.scatterplot)
        g.map_lower(sns.kdeplot, fill=True)
        g.map_diag(sns.histplot, kde=True)
        return g.figure

    def get_plots(self):
        return {
            f'{"_".join(func.__name__.split("_")[1:])}' : func() 
                        for func in self.all_plots_funs
        }

class DrawerPlots:
    def __init__(self, plots : dict) -> None:
        self.plots = plots

    def draw(self):
        plt.show()

class JSONImporter:
    def __init__(self, path : str) -> None:
        self.path = path

    def import_(self, *args: Any, **kwds: Any) -> dict:
        return pd.read_json(self.path)

class PlotsSaver:
    def __init__(self, plots : dict) -> None:
        self.plots = plots

    def save(self, path='/', *args: Any, **kwds: Any) -> Any:
        for plot_name, plot in self.plots.items():
            plot.savefig(f'{path}/{plot_name}.png')



