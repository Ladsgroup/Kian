import json
import codecs
import os


class Model(object):
    """docstring for Model"""
    def __init__(self, name, wiki, property_name, value, bias_unit=None):
        self.name = name
        self.wiki = wiki
        self.property_name = property_name
        self.value = value
        path = os.path.dirname(os.path.realpath(__file__))
        self.data_directory = os.path.abspath(
            os.path.join(path, os.pardir, 'data',
                         '%s' % self.name))
        if bias_unit:
            self.bias_unit = bias_unit

    @classmethod
    def from_file(cls, name):
        path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.abspath(
            os.path.join(path, os.pardir, 'models',
                         '%s.json' % name))
        if not os.path.isfile(file_path):
            raise RuntimeError('File could not be found!')
        with codecs.open(file_path, 'r', 'utf-8') as f:
            content = json.loads(f.read())
        model = cls(**content)
        return model

    def write_file(self, force=False):
        path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.abspath(
            os.path.join(path, os.pardir, 'models',
                         '%s.json' % self.name))
        print(file_path)
        if os.path.isfile(file_path) and not force:
            raise RuntimeError('File is there!')
        content = {}
        content['name'] = self.name
        content['wiki'] = self.wiki
        content['property_name'] = self.property_name
        content['value'] = self.value
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(json.dumps(content))
