from os import walk, path
from os import name as os_name
import pygame


def import_folder(input_path):
    # surface_list = []
    paths_list = []

    # print('------')
    # print(input_path)

    for _, __, img_files in walk(input_path):
        # print(img_files)
        for image in img_files:
            # print(image)
            full_path = path.join(input_path, image)
            # print(full_path)
            paths_list.append(full_path)
            # image_surf = pygame.image.load(full_path).convert_alpha()
            # surface_list.append(image_surf)

    # print(surface_list)
    # print('------')
    paths_list.sort(key=lambda x: path.basename(x))

    # print('------')
    # print(paths_list)
    # print('------')

    surface_list = [
        pygame.image.load(item).convert_alpha() for item in paths_list
    ]

    return surface_list


def import_folder_dict(input_path):
    surface_dict = {}

    for _, __, img_files in walk(input_path):
        for image in img_files:
            full_path = path.join(input_path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    return surface_dict


def import_folder_dict2(input_path):
    surface_dict = {}

    for wrong_path, files, img_files in walk(input_path):
        imgs_lst = []
        actual_path = wrong_path.split('\\')[-1]
        for image in img_files:
            # path old: path + '/' + actual_path + '/' + image
            # ubuntu path actual_path + '/' + image
            if os_name == 'nt':  # Windows
                full_path = path.join(input_path, actual_path, image)
            else:
                full_path = path.join(actual_path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            imgs_lst.append(image_surf)
        if not files:
            # second .split is a fix for linux (ubuntu)
            surface_dict[actual_path.split('/')[-1]] = imgs_lst

    return surface_dict
