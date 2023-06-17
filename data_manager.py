import constant
import copy
from flask import abort
from csv_manager import get_data, update_data


def init_data():
    return get_data()


def get_by_phone_number(phone_number, repo):
    name_list_response = []
    filtered_names = repo.data[(repo.data.phone_number == phone_number)].name
    if not filtered_names.empty:
        for name in filtered_names:
            name_list_response.append("full_name: {}".format(name))
    return name_list_response


def delete_by_phone_number(phone_number, repo):
    index_to_delete = repo.data[(repo.data.phone_number == phone_number)].index
    if not index_to_delete.empty:
        handle_delete(index_to_delete, repo)
    else:
        abort(400, "The phone number did not exist")


def updateDataBase(updated_data):
    updated_data.to_csv(constant.FILE_PATH, index=False, mode='w')


def handle_delete(index_to_delete, repo):
    updated_data = copy.deepcopy(repo.data)
    updated_data.drop(index_to_delete, inplace=True)
    try:
        update_data(updated_data)
    except:
        abort(500, "Error saving new data to Database")
    else:
        repo.data = copy.deepcopy(updated_data)
