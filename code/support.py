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

    for wrong_path, __, img_files in walk(path):
        imgs_lst = []
        actual_path = wrong_path.split('\\')[-1]
        for image in img_files:
            full_path = path + '/' + actual_path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            imgs_lst.append(image_surf)

        surface_dict[actual_path] = imgs_lst

    return surface_dict

def get_stats(path):
    """
    >>> get_stats('../data/player_info.csv')
    [0, 0, 30, 60, 60, 50]
    """
    f = open(path)
    f.readline()
    f.readline()
    f.readline()
    info_lst = []
    for ln in f:
        curr_line = ln.split(',')
        curr_line[-1] = curr_line[-1]
        info_lst.append(curr_line)
    f.close()
    return [[int(stat) for stat in element] for element in info_lst]


