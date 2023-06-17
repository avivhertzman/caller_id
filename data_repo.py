class dataRepo:
    def __init__(self, data):
        self._data = data

    def _get_data(self):
        return self._data;

    def _set_data(self, value):
        self._data = value;

    data = property(fget=_get_data, fset=_set_data)