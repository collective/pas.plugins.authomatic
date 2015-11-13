# -*- coding: utf-8 -*-


class MockResult(dict):

    def __init__(self, *args, **kwargs):
        super(MockResult, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def to_dict(self):
        return self


class MockCredentials(MockResult):

    def refresh(*args):
        pass
