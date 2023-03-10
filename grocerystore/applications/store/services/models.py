import os.path
import shutil
from typing import NamedTuple

import lorem
from PIL import Image
from django.core.validators import MaxValueValidator
from django.db import models as m

from . import config

params = {'default': 120, 'validators': [MaxValueValidator(limit_value=999)],
          'help_text': 'per_100_grams', }

sizes = {'_extra_small.': config.XS_PHOTO_SIZE,
         '_small.': config.S_PHOTO_SIZE,
         '_middle.': config.M_PHOTO_SIZE}


def get_photo_path_for_product(product, photo):
    return f"photos/products/{product.category.name}/{product.name}/{photo}"


def get_photo_path_for_category(category, photo):
    return f"photos/categories/{category.name}/{photo}"


def create_description():
    sentence0 = lorem.sentence()
    sentence1 = lorem.sentence()
    return sentence0 + " " + sentence1


class PhotoPath(NamedTuple):
    photo: str
    path: str


class PhotoAbstractModel(m.Model):
    class Meta:
        abstract = True

    photo = m.ImageField()

    def get_extra_small_photo(self) -> str:
        size = '_extra_small.'
        return self.__get_photo(size)

    def get_miniature_photo(self) -> str:
        size = '_small.'
        return self.__get_photo(size)

    def get_middle_sized_photo(self) -> str:
        size = '_middle.'
        return self.__get_photo(size)

    def delete_all_instance_photos(self) -> None:
        result = self.__get_photo_name_and_path()
        shutil.rmtree(result.path)

    def __get_photo(self, size: str) -> str:
        result = self.__get_photo_name_and_path()
        if self.__replace_dot_in_str(result.photo, size) in \
                os.listdir(result.path):
            return self.__replace_dot_in_str(self.photo.url, size)
        else:
            return self.__create_photo(size)

    def __get_photo_name_and_path(self) -> PhotoPath:
        photo_name = os.path.basename(self.photo.name)
        path = self.photo.path.rstrip(photo_name)

        return PhotoPath(photo=photo_name, path=path)

    def __create_photo(self, size: str) -> str:
        with Image.open(self.photo.path) as img:
            new_img = img.resize(sizes[size])
            new_img.save(self.__replace_dot_in_str(self.photo.path, size))
            return self.__replace_dot_in_str(self.photo.url, size)

    @staticmethod
    def __replace_dot_in_str(str_: str, size: str) -> str:
        return str_.replace('.', size)
