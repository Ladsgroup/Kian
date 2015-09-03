import json
import os
import codecs
from kian.parser import ModelWithData


class TrainedModel(ModelWithData):
    """docstring for TrainedModel"""
    def __init__(self, *args, **kwargs):
        super(TrainedModel, self).__init__(*args, **kwargs)
        file_path = os.path.join(
            self.data_directory, 'categories.json')
        if not os.path.isfile(file_path):
            raise ValueError('You should train the model first')
        file_path = os.path.join(
            self.data_directory, 'theta.dat')
        if not os.path.isfile(file_path):
            raise ValueError('You should train the model first')

    def load_categories(self):
        file_path = os.path.join(
            self.data_directory, 'categories.json')
        with codecs.open(file_path, 'r', 'utf-8') as f:
            self.categories = json.loads(f.read())

    def load_theta(self):
        file_path = os.path.join(
            self.data_directory, 'theta.dat')
        with codecs.open(file_path, 'r', 'utf-8') as f:
            self.theta = eval(f.read())

    def load(self):
        self.load_categories()
        self.load_theta()
