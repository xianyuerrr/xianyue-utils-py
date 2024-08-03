import types


def serialize_obj(obj):
    """
    序列化对象函数，将对象转换为字典或列表的形式

    参数:
        obj: 需要序列化的对象

    返回:
        序列化后的对象
    """
    if isinstance(obj, dict):
        return {k: serialize_obj(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return {
            k: serialize_obj(v)
            for k, v in obj.__dict__.items()
            if not callable(v) and not k.startswith("_")
        }
    elif isinstance(obj, list):
        return [serialize_obj(elem for elem in obj)]
    elif isinstance(obj, types.GeneratorType):
        return list(obj).sort()
    elif isinstance(obj, set):
        return list(obj).sort()
    else:
        return obj
