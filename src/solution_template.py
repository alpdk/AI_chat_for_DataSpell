import csv
import sys
import pandas as pd
from DataFrameTransformer import DataFrameTransformer


def change_and_save_df(dataframe_name: str, save_df_path: str):
    df = pd.read_csv(dataframe_name)

    df_transformer = DataFrameTransformer(df)

    ### There should be your dataframe changes

    new_df = df_transformer.get_result()

    with open(save_df_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_df)


def main():
    argv = sys.argv
    dataframe_name = "../dataframes/Housing.csv"
    save_df_path = "../dataframes/Housing_Modified.csv"

    if len(argv) == 2:
        dataframe_name = argv[1]
    elif len(argv):
        dataframe_name = argv[1]
        save_df_path = argv[2]
    elif len(argv) > 3:
        print("Error: Incorrect number of arguments! There should be no more than 2 arguments!")
        return 1

    change_and_save_df(dataframe_name, save_df_path)

    return 0


if __name__ == '__main__':
    main()
