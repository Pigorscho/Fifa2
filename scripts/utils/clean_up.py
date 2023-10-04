import os
import clipboard

from settings import settings


def clear_clipboard():
    clipboard.copy('')


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except PermissionError:
        print(f"Permission denied. Couldn't delete {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def clean_up():
    for key, val in settings.items():
        delete_file(rf"pics\screen-{val['port']}.png")


def clean_single(port):
    delete_file(rf'pics\screen-{port}.png')
