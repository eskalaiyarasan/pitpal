class IllegalOperation(Exception):
    pass


class IllegalConfiguration(Exception):
    pass


def check_enabled_ret_value(data):
    if data["Param"]["Enabled"]:
        return data["Param"]["Value"]
    else:
        return data["Param"]["Default"]
