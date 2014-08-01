from collections import OrderedDict


def set_op(**kwargs):
    return lambda data: dict(data, **kwargs)


class Pipeline(object):
    def __init__(self, *args, **kwargs):
        self.od = OrderedDict(*args, **kwargs)

    def __iter__(self):
        return self.od.itervalues()

    def prepend(self, **kwargs):
        """
        Adds the specified operations to the beginning of the pipeline
        Note: if the key is duplicated, your value will be lost, and the old value will stay
        :param kwargs: key should be string, and value should be callable with arity of 1 taking the data object
        :return: new Pipeline object
        """
        return Pipeline(kwargs.items() + self.od.items())

    def append(self, **kwargs):
        """
        Adds the specified operations to the end of the pipeline
        Note: if the key is duplicated, your value will replace the old value
        :param kwargs: key should be string, and value should be callable with arity of 1 taking the data object
        :return: new Pipeline object
        """
        return Pipeline(self.od, **kwargs)

    def before(self, key, **kwargs):
        """
        Inserts the specified operations to the pipeline, right before the specified key
        :param key: string,
        :param kwargs: key should be string, and value should be callable with arity of 1 taking the data object
        :return: new Pipeline object
        """
        index = self.od.keys().index(key)
        items = self.od.items()
        return Pipeline(items[:index] + kwargs.items() + items[index:])