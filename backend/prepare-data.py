import os
import shutil
from os import mkdir
from zipfile import ZipFile


def unzip_maestro_data():
    with ZipFile("./data-raw/maestro-v3.0.0-midi.zip", "r") as zip_object:
        zip_object.extractall(path="./data/maestro")
    shutil.copyfile("./data-raw/maestro-v3.0.0.csv", "./data/maestro/maestro.csv")


def prepare_data_folder():
    try:
        os.rmdir("data")
    except FileExistsError:
        pass
    except Exception as ex:
        print(ex)

    try:
        os.mkdir("data")
        os.mkdir("data/maestro")
    except FileExistsError:
        pass
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    prepare_data_folder()
    unzip_maestro_data()

