import os


def get_project_absolute_path(*args):
    project_root = os.getcwd()

    # 基于根目录的文件路径
    file_path = os.path.join(project_root, *args)
    return file_path