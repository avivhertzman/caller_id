import constant
import copy
import pandas as pd
from flask import Flask, jsonify, abort, request, make_response, url_for


# class dataRepo:
#     def _init(self, data):
#         self._data = data;
#
#     def _get_data(self):
#         return self._data;
#
#     def _set_data(self, value):
#         self._data = value;
#
#     data = property(fget=_get_data(), fset=_set_data()   )


def init_data():
    global data
    data = pd.read_csv(constant.FILE_PATH, nrows=30)


def get_by_phone_number(phone_number):
    name_list_response = []
    if not data[(data.phone_number == phone_number)].name.empty:
        name_list_filtered = data[(data.phone_number == phone_number)].name
        for name in name_list_filtered:
            name_list_response.append("full_name: {}".format(name))
    return name_list_response


def delete_by_phone_number(phone_number):
    index_to_delete = data[(data.phone_number == phone_number)].index
    if not index_to_delete.empty:
        handle_delete(index_to_delete)
    else:
        abort(400, "The phone number did not exist")

def updateDataBase():
    data.to_csv(constant.FILE_PATH, index=False, mode='w')

def handle_delete(index_to_delete):
    global data
    curr_data = copy.deepcopy(data)
    data.drop(index_to_delete, inplace=True)
    try:
        updateDataBase()
    except:
        data = copy.deepcopy(curr_data)
        abort(500, "Error saving new data to Database")
