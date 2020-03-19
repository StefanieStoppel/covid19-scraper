import pandas as pd
import os
import matplotlib.pyplot as plt
from src.util.utils import get_project_root


class Plotter:
    data_dir = os.path.join(str(get_project_root()), 'data')

    def create_wiki_dataframe(self):
        file_path = os.path.join(self.data_dir, 'wiki-covid-19-germany-2020-02-24--2020-03-16.txt')
        return pd.read_csv(file_path, header=0, index_col=0, thousands='.', sep='\t') \
            .replace(u'\u2014', 0) \
            .transpose() \
            .astype(float)

    @staticmethod
    def display_county_histogram(df):
        print(df.columns)
        df.plot(kind='line', logy=True, ylim=(10, df['Gesamt'].max() + 1000))
        plt.legend(loc='upper left', ncol=2)
        plt.show()


if __name__ == "__main__":
    dw = Plotter()
    dw.display_county_histogram(dw.create_wiki_dataframe())
