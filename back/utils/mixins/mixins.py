import dataclasses


class SingletonMixin(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMixin, cls).__call__(*args,
                                                                      **kwargs)
        return cls._instances[cls]


@dataclasses.dataclass()
class DataMixin:

    def to_dict(self):
        return dataclasses.asdict(self)