
from dataclasses import is_dataclass, fields
from typing import get_origin, get_args

class ConfigConvertor:

    @staticmethod
    def config_from_dict(dataclass_type, data: dict):

        if not is_dataclass(dataclass_type):
            return data

        kwargs = {}

        for field in fields(dataclass_type):

            value = data.get(field.name)

            if value is None:
                kwargs[field.name] = None
                continue

            field_type = field.type
            origin = get_origin(field_type)

            # list handling
            if origin == list:
                item_type = get_args(field_type)[0]

                if is_dataclass(item_type):
                    kwargs[field.name] = [
                         ConfigConvertor.config_from_dict(item_type, v) for v in value
                    ]
                else:
                    kwargs[field.name] = value

            # nested dataclass
            elif is_dataclass(field_type):
                kwargs[field.name] =  ConfigConvertor.config_from_dict(field_type, value)

            else:
                kwargs[field.name] = value

        return dataclass_type(**kwargs)

