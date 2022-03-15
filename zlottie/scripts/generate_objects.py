from pydantic import BaseModel
import importlib
import inspect

imports = "from zlottie.base import LottieObject, LottieAttribute\nfrom typing import Optional\n\n"
class_template = "class {0}({1}):\n"

# e.g.: "    author: Optional[str] = LottieAttribute(tag='a', description='Author')"
attr_template = "    {0}: {1} = LottieAttribute(tag='{2}', description='{3}')\n"
attr_with_default_template = "    {0}: {1} = LottieAttribute(tag='{2}', default={3}, description='{4}')\n"

optional_attr_template = "    {0}: Optional[{1}] = LottieAttribute(tag='{2}', description='{3}')\n"
optional_attr_with_default_template = "    {0}: Optional[{1}] = LottieAttribute(tag='{2}', default={3}, description='{4}')\n"


def _extract_own_fields(model):
    subclass_attributes = []
    for cls in model.__bases__:
        if issubclass(cls, BaseModel):
            subclass_attributes.extend(cls.__fields__.keys())
    own_fields = {k: v for k, v in model.__fields__.items() if k not in subclass_attributes}
    return own_fields


def _format_attributes(fields):
    lines = []
    for key, field in fields.items():
        tag = key
        name = field.field_info.title if field.field_info.title else tag
        name = name.replace(' ', '_').lower()
        try:
            type_ = field.type_.__name__
        except AttributeError:
            type_ = field.type_
        default = field.default
        description = field.field_info.description or field.field_info.title
        if default is not None:
            template = attr_with_default_template if field.required else optional_attr_with_default_template
            line = template.format(name, type_, tag, default, description)
        else:
            template = attr_template if field.required else optional_attr_template
            line = template.format(name, type_, tag, description)
        lines.append(line)
    return lines


def generate_lottie_object(model):
    lines = [imports]
    # class statement
    classes = ', '.join(b.__name__ for b in model.__bases__)
    classes = classes.replace('BaseModel', 'LottieObject')
    lines.append(class_template.format(model.__name__, classes))
    # attributes
    own_fields = _extract_own_fields(model)
    if own_fields:
        attributes = _format_attributes(own_fields)
    else:
        attributes = ['    pass\n']
    lines.extend(attributes)
    return lines


if __name__ == '__main__':
    module = importlib.import_module('models.lottie')
    # lines = generate_lottie_object(module.TransformModel)

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, BaseModel):
            filename = f'./output/{obj.__name__}.py'
            lines = generate_lottie_object(obj)
            with open(filename, 'wt') as f:
                f.writelines(lines)
