# -*- coding: utf-8 -*-
class EnumType(object):
    def __init__(self, value, desc):
        self.value = value
        self.desc = desc


class MetaEnum(type):
    def __new__(cls, name, bases, attrs):
        if name != 'MetaEnum':
            enum_choices = []
            enum_desc_dict = {}
            enum_value_dict = {}
            for k, v in attrs.items():
                if isinstance(v, EnumType):
                    enum_choices.append((v.value, v.desc))
                    enum_desc_dict.update({v.value: v.desc})
                    enum_value_dict.update({k: v.value})
            attrs.update({
                'ENUM_CHOICES': tuple(enum_choices),
                'ENUM_DESC_DICT': enum_desc_dict
            })
            attrs.update(enum_value_dict)
        new_cls = super(MetaEnum, cls).__new__(cls, name, bases, attrs)
        return new_cls


class BaseEnum(object):
    __metaclass__ = MetaEnum

    ENUM_CHOICES = ()  # 字段choices
    ENUM_DESC_DICT = {}  # 描述字段

    @classmethod
    def display(cls, value):
        return cls.ENUM_DESC_DICT.get(value, value)