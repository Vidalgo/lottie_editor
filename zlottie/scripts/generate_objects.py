from pydantic import BaseModel
import importlib
import inspect

imports = "from zlottie.base import LottieObject, LottieAttribute"
class_template = "class {0}({1}):"

# e.g.: "    author: Optional[str] = LottieAttribute(tag='a', description='Author')"
attr_template = "    {0}: [{1}] = LottieAttribute(tag='{0}', description='{2}')"
optional_attr_template = "    {0}: Optional[{1}] = LottieAttribute(tag='{0}', description='{2}')"


def generate_lottie_object(model):
    lines = [imports, '', '']
    # class statement
    classes = ', '.join(b.__name__ for b in model.__bases__)
    classes = classes.replace('BaseModel', 'LottieObject')
    lines.append(class_template.format(model.__name__, classes))
    # attributes
    for key, field in model.__fields__.items():
        tag = key
        try:
            type_ = field.type_.__name__ # field.outer_type_.__name__
        except AttributeError:
            type_ = field.type_
        description = field.field_info.description or field.field_info.title
        template = attr_template if not field.required else optional_attr_template
        line = template.format(tag, type_, description)
        lines.append(line)
    lines.append('')
    return [f'{l}\n' for l in lines]


if __name__ == '__main__':
    module = importlib.import_module('models.lottie')
    #lines = generate_lottie_object(module.Animation)

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, BaseModel):
            filename = f'./output/{obj.__name__}.py'
            lines = generate_lottie_object(obj)
            with open(filename, 'wt') as f:
                f.writelines(lines)
