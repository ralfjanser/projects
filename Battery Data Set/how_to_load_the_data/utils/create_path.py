import os


def get_folders_path(filepath):
    currentFolder = os.path.dirname(filepath)
    folders = [currentFolder]

    while currentFolder != '':
        folders.append(currentFolder)
        currentFolder = os.path.dirname(currentFolder)

    return folders


def create_folder(folder):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass


def create_path(filepath):
    folders = get_folders_path(filepath)

    [create_folder(folder) for folder in folders]
