import os.path

from PIL import Image
from django.core.validators import MaxValueValidator
from django.db import models as m

from app import settings as st

params = {'default': 120, 'validators': [MaxValueValidator(limit_value=999)],
          'help_text': 'per_100_grams', }

sizes = {'_small.': st.MINIATURE_PHOTO_SIZE,
         '_middle.': st.MIDDLE_PHOTO_SIZE}


def get_photo_path_for_product(product, photo):
    return f"photos/products/{product.category.name}/{product.name}/{photo}"


def get_photo_path_for_category(category, photo):
    return f"photos/categories/{category.name}/{photo}"


class InstanceImage:
    photo = m.ImageField()

    def get_miniature_photo(self):
        size = '_small.'
        return self.__get_photo(size)

    def get_middle_sized_photo(self):
        size = '_middle.'
        return self.__get_photo(size)

    def __get_photo(self, size: str):
        photo_name, file_path = self.__get_photo_name_and_path()
        if self.__replace_dot_in_str(photo_name, size) in \
                os.listdir(file_path):
            return self.__replace_dot_in_str(self.photo.url, size)
        else:
            return self.__create_photo(size)

    def __get_photo_name_and_path(self):
        photo_name = os.path.basename(self.photo.name)
        return photo_name, self.photo.path.rstrip(photo_name)

    def __create_photo(self, size: str):
        with Image.open(self.photo.path) as img:
            new_img = img.resize(sizes[size])
            new_img.save(self.__replace_dot_in_str(self.photo.path, size))
            return self.__replace_dot_in_str(self.photo.url, size)

    @staticmethod
    def __replace_dot_in_str(str_: str, size: str):
        return str_.replace('.', size)
