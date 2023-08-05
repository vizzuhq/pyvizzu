"""
This module provides the `NumpyArrayConverter` class,
which allows converting a `numpy` `array`
into a list of dictionaries representing series.
"""

from types import ModuleType
from typing import Dict, List, Optional, Tuple, Type, Union

from ipyvizzu.data.converters.converter import ToSeriesListConverter
from ipyvizzu.data.converters.numpy.type_alias import ColumnName, ColumnDtype
from ipyvizzu.data.infer_type import InferType
from ipyvizzu.data.type_alias import (
    DimensionValue,
    MeasureValue,
    Series,
    SeriesValues,
)


class NumpyArrayConverter(ToSeriesListConverter):
    """
    Converts a `numpy` `array` into a list of dictionaries representing series.
    Each dictionary contains information about the series `name`, `values` and `type`.

    Parameters:
        np_array: The `numpy` `array` to convert.
        column_name:
            The name of a column. By default, uses column indices. Can be set with an
            Index:Name pair or, for single-dimensional arrays, with just the Name.
        column_dtype:
            The dtype of a column. By default, uses the np_array's dtype. Can be set
            with an Index:DType pair or, for single-dimensional arrays, with just the DType.
        default_measure_value:
            Default value to use for missing measure values. Defaults to 0.
        default_dimension_value:
            Default value to use for missing dimension values. Defaults to an empty string.

    Example:
        Get series list from `numpy` `array`:

            converter = NumpyArrayConverter(np_array)
            series_list = converter.get_series_list()
    """

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        np_array: Optional["np.array"],  # type: ignore
        column_name: Optional[ColumnName] = None,
        column_dtype: Optional[ColumnDtype] = None,
        default_measure_value: Optional[MeasureValue] = 0,
        default_dimension_value: Optional[DimensionValue] = "",
    ) -> None:
        # pylint: disable=too-many-arguments

        self._np = self._get_numpy()
        self._np_array = np_array
        self._column_name = self._get_settings(column_name)
        self._column_dtype = self._get_settings(column_dtype)
        self._default_measure_value = default_measure_value
        self._default_dimension_value = default_dimension_value

    def get_series_list(self) -> List[Series]:
        """
        Convert the `numpy` `array` to a list of dictionaries representing series.

        Returns:
            A list of dictionaries representing series,
            where each dictionary has `name`, `values` and `type` keys.
        """

        if isinstance(self._np_array, type(None)) or self._np_array.ndim == 0:  # type: ignore
            return []
        if self._np_array.ndim == 1:  # type: ignore
            return self._get_series_list_from_array1dim()
        if self._np_array.ndim == 2:  # type: ignore
            return self._get_series_list_from_array2dim()
        raise ValueError("arrays larger than 2D are not supported")

    def _get_series_list_from_array1dim(self) -> List[Series]:
        i = 0
        name = self._column_name.get(i, i)
        values, infer_type = self._convert_to_series_values_and_type(
            (i, self._np_array)
        )
        return [self._convert_to_series(name, values, infer_type)]

    def _get_series_list_from_array2dim(self) -> List[Series]:
        series_list = []
        for i in range(self._np_array.shape[1]):  # type: ignore
            name = self._column_name.get(i, i)
            values, infer_type = self._convert_to_series_values_and_type(
                (i, self._np_array[:, i])  # type: ignore
            )
            series_list.append(self._convert_to_series(name, values, infer_type))
        return series_list

    def _get_numpy(self) -> ModuleType:
        try:
            import numpy as np  # pylint: disable=import-outside-toplevel

            return np
        except ImportError as error:
            raise ImportError(
                "numpy is not available. Please install numpy to use this feature."
            ) from error

    def _get_settings(
        self, config: Optional[Union[ColumnName, ColumnDtype]]
    ) -> Union[Dict[int, str], Dict[int, Type]]:
        if isinstance(config, type(None)):
            return {}
        if not isinstance(config, dict):
            if not self._np_array.ndim == 1:
                raise ValueError("non dict value can only be used for a 1D array")
            return {0: config}
        return config

    def _convert_to_series_values_and_type(
        self, obj: Tuple[int, "np.array"]  # type: ignore
    ) -> Tuple[SeriesValues, InferType]:
        column = obj
        i = column[0]
        array = column[1]
        dtype = self._column_dtype.get(i, self._np_array.dtype)  # type: ignore
        if self._np.issubdtype(dtype, self._np.number):
            return self._convert_to_measure_values(array), InferType.MEASURE
        return self._convert_to_dimension_values(array), InferType.DIMENSION

    def _convert_to_measure_values(self, obj: "np.array") -> List[MeasureValue]:  # type: ignore
        array = obj
        array_float = array.astype(float)
        return self._np.nan_to_num(
            array_float, nan=self._default_measure_value
        ).tolist()

    def _convert_to_dimension_values(self, obj: "np.array") -> List[DimensionValue]:  # type: ignore
        array = obj
        array_str = array.astype(str)
        replace_nan = "nan"
        mask = array_str == replace_nan
        array_str[mask] = self._default_dimension_value
        return array_str.tolist()