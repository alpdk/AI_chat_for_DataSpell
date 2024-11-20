import sys
import pandas as pd
from DataFrameTransformer import DataFrameTransformer


def change_and_save_df(dataframe_name: str, save_df_path: str):
    df = pd.read_csv(dataframe_name)

    df_transformer = DataFrameTransformer(df)

    ### There should be your dataframe changes

    new_df = df_transformer.get_result()

    new_df.to_csv(f'{save_df_path}', index=False)


def main():
    argv = sys.argv

    if not (len(argv) <= 3):
        print("Error: Incorrect number of arguments! There should be between 0 and 2 arguments.")
        return None

    dataframe_name = argv[1] if len(argv) >= 2 else "../dataframes/Housing.csv"
    save_df_path = argv[2] if len(argv) >= 3 else "../dataframes/Housing_Modified.csv"

    change_and_save_df(dataframe_name, save_df_path)


if __name__ == '__main__':
    main()
