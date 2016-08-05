from .category import CategoricalIndex
from pandas.core.strings import StringAccessorMixin
from pandas.types.common import is_scalar, is_pandas_string_dtype
from pandas.types.generic import ABCString



class StringIndex(CategoricalIndex, StringAccessorMixin):

    _typ = 'stringindex'

    def __new__(cls, data=None, dtype=None,
                copy=False, name=None, fastpath=False, **kwargs):

        if fastpath:
            return cls._simple_new(data, name=name)

        if name is None and hasattr(data, 'name'):
            name = data.name

        if isinstance(data, ABCString):
            data = cls._create_internal(cls, data)
        elif isinstance(data, StringIndex):
            data = data._data
            data = cls._create_internal(cls, data)
        else:

            # don't allow scalars
            # if data is None, then categories must be provided
            if is_scalar(data):
                if data is not None or categories is None:
                    cls._scalar_data_error(data)
                data = []
            data = cls._create_internal(cls, data)

        if copy:
            data = data.copy()

        return cls._simple_new(data, name=name)

    @staticmethod
    def _create_internal(self, data, categories=None, ordered=None):
        """
        *this is an internal non-public method*

        create the correct categorical from data and the properties

        Parameters
        ----------
        data : data for new String
        categories : not used, for CategoricalIndex compat
        ordered : not used, for CategoricalIndex compat

        Returns
        -------
        String
        """
        if not isinstance(data, ABCString):
            from pandas.core.strings import String
            try:
                data = String(data)
            except ValueError:
                raise

        return data

    def _is_dtype_compat(self, other):
        """
        *this is an internal non-public method*

        provide a comparison between the dtype of self and other (coercing if
        needed)

        Raises
        ------
        TypeError if the dtypes are not compatible
        """
        if is_pandas_string_dtype(other):
            if isinstance(other, StringIndex):
                other = other._values
        else:
            if not is_list_like(other):
                other = [values]
            other = StringIndex(other)
        return other


    def _init_internal_attrs(self):
        return []

    @property
    def inferred_type(self):
        return 'string'

    @classmethod
    def _add_accessors(cls):
        """ add in Categorical accessor methods """

        from pandas.core.strings import String
        StringIndex._add_delegate_accessors(
            delegate=String, accessors=["upper", "lower"],
            typ='method', overwrite=True)


# StringIndex._add_accessors()

