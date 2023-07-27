from os import walk
import pygame


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    return surface_dict


def import_folder_dict2(path):
    surface_dict = {}

    for wrong_path, files, img_files in walk(path):
        imgs_lst = []
        actual_path = wrong_path.split('\\')[-1]
        for image in img_files:
            # path old: path + '/' + actual_path + '/' + image
            # ubuntu path actual_path + '/' + image
            full_path = path + '/' + actual_path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            imgs_lst.append(image_surf)
        if not files:
            # second .split is a fix for linux (ubuntu)
            surface_dict[actual_path.split('/')[-1]] = imgs_lst

    return surface_dict
