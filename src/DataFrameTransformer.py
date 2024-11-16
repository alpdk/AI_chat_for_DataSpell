import pandas as pd

class DataFrameTransformer:
    """
    Transforms a Pandas DataFrame with methods like cleaning column names,
    filtering rows, and selecting columns. The original DataFrame remains unchanged.
    """

    def __init__(self, df : pd.DataFrame):
        """
        Initializes with a copy of the input DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame to transform.
        """
        self.df: pd.DataFrame = df.copy()

    def select_columns(self, columns: list[str]):
        """
        Selects specified columns from the DataFrame.

        Args:
            columns (list): The column names to select.

        Returns:
            DataFrameTransformer: The instance with selected columns.

        Raises:
            ValueError: If any columns are missing.
        """
        # Take columns that do not exist in dataframe but exist in selected
        missing_cols = [col for col in columns if col not in self.df.columns]

        # Ensure there are no missing columns
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        self.df = self.df[columns]
        return self

    def filter_by_condition(self, condition: callable):
        """
        Filters rows based on a condition function.

        Args:
            condition (callable): A function returning a boolean Series or list.

        Returns:
            DataFrameTransformer: The instance with filtered rows.

        Raises:
            ValueError: If the condition does not return a boolean Series or list.
        """
        # Get the boolean mask from the condition
        boolean_result = condition(self.df)

        if isinstance(boolean_result, list):
            boolean_result = pd.Series(boolean_result, index=self.df.index)
        elif not isinstance(boolean_result, pd.Series):
            raise ValueError("Condition must return a boolean Series or list.")

        self.df = self.df[boolean_result]
        return self

    def get_result(self):
        """
        Returns the transformed DataFrame.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """
        return self.df
