"""
This module provides the `PandasDataFrameConverter` class,
which allows converting a `pandas` `DataFrame` or `Series`
into a list of dictionaries representing series.
"""

from types import ModuleType
from typing import List, Optional, Tuple, Union

from ipyvizzu.data.infer_type import InferType
from ipyvizzu.data.typing_alias import (
    DimensionValue,
    MeasureValue,
    Series,
    SeriesValues,
)


class PandasDataFrameConverter:
    """
    Converts a `pandas` `DataFrame` or `Series` into a list of dictionaries representing series.
    Each dictionary contains information about the series `name`, `values` and `type`.

    Parameters:
        df: The `pandas` `DataFrame` or `Series` to convert.
        default_measure_value:
            Default value to use for missing measure values. Defaults to 0.
        default_dimension_value:
            Default value to use for missing dimension values. Defaults to an empty string.
        include_index:
            Name for the index column to include as a series.
            If provided, the index column will be added. Defaults to None.

    Example:
        Get series list from `DataFrame` columns:

            converter = PandasDataFrameConverter(df)
            series_list = converter.get_series_list_from_columns()
    """

    def __init__(
        self,
        df: Optional[Union["pd.DataFrame", "pd.Series"]],  # type: ignore
        default_measure_value: Optional[MeasureValue] = 0,
        default_dimension_value: Optional[DimensionValue] = "",
        include_index: Optional[str] = None,
    ) -> None:
        self._pd = self._get_pandas()
        self._df = self._get_df(df)
        self._default_measure_value = default_measure_value
        self._default_dimension_value = default_dimension_value
        self._include_index = include_index

    def _get_pandas(self) -> ModuleType:
        try:
            import pandas as pd  # pylint: disable=import-outside-toplevel

            return pd
        except ImportError as error:  # pragma: no cover
            raise ImportError(
                "pandas is not available. Please install pandas to use this feature."
            ) from error

    def _get_df(self, df: Union["pd.DataFrame", "pd.Series"]) -> "pd.DataFrame":  # type: ignore
        if isinstance(df, self._pd.DataFrame):
            return df
        if isinstance(df, self._pd.Series):
            return self._pd.DataFrame(df)
        if isinstance(df, type(None)):
            return self._pd.DataFrame()
        raise TypeError("df must be an instance of pandas.DataFrame or pandas.Series")

    def get_series_list_from_columns(self) -> List[Series]:
        """
        Convert the `DataFrame` columns to a list of dictionaries representing series.

        Returns:
            A list of dictionaries representing series,
            where each dictionary has `name`, `values` and `type` keys.
        """

        series_list = []
        index_series = self.get_series_from_index()
        if index_series:
            series_list.append(index_series)
        for name in self._df.columns:
            series_list.append(self._get_series_from_column(name))
        return series_list

    def get_series_from_index(self) -> Optional[Series]:
        """
        Convert the `DataFrame` index to a dictionary representing a series,
        if `include_index` is provided.

        Returns:
            A dictionary representing the index series with `name`, `values` and `type` keys.
            Returns `None` if `include_index` is not provided.
        """

        if not self._include_index or self._df.index.empty:
            return None
        name = self._include_index
        values, infer_type = self._get_column_data(self._df.index)
        return self._convert_to_series(name, values, infer_type)

    def _get_series_from_column(self, column_name: str) -> Series:
        column = self._df[column_name]
        values, infer_type = self._get_column_data(column)
        return self._convert_to_series(column_name, values, infer_type)

    def _get_column_data(
        self, column: "pd.Series"  # type: ignore
    ) -> Tuple[SeriesValues, InferType]:
        if self._pd.api.types.is_numeric_dtype(column.dtype):
            return self._get_measure_column_data(column)
        return self._get_dimension_column_data(column)

    def _get_measure_column_data(
        self, column: "pd.Series"  # type: ignore
    ) -> Tuple[List[MeasureValue], InferType]:
        return (
            column.fillna(self._default_measure_value).astype(float).values.tolist(),
            InferType.MEASURE,
        )

    def _get_dimension_column_data(
        self, column: "pd.Series"  # type: ignore
    ) -> Tuple[List[DimensionValue], InferType]:
        return (
            column.fillna(self._default_dimension_value).astype(str).values.tolist(),
            InferType.DIMENSION,
        )

    def _convert_to_series(
        self, name: str, values: SeriesValues, infer_type: InferType
    ) -> Series:
        return {
            "name": name,
            "values": values,
            "type": infer_type.value,
        }
