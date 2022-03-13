from typing import Any, Union, List, get_args, get_origin


class LottieAttribute:
    _clone_attrs = ['_name', '_tag', '_annotation', '_description', '_autoload']
    _eq_attrs = ['_name', '_tag', '_annotation']

    def __init__(self, **kwargs):
        """
        Initializes a new LottieAttribute object.
        All parameters are optional, but should not be modified after instantiation.
        Instead, use the clone() method to create a clone, and change parameters

        Args:
            name (str): attribute name as appears in the class. Default: None
            tag (str): attribute lottie tag ("w", "h", "fr" etc.). Default: None
            annotation (Any): type annotation. Default: None
            description (str): attribute description. Default: ''

        The type parameter is parsed is used to extract several LottieAttribute properties. For example:
        type =

        """
        # given attrs
        self._name = kwargs.get('name')
        self._tag = kwargs.get('tag')
        self._annotation = kwargs.get('annotation')
        self._description = kwargs.get('description')
        self._autoload = kwargs.get('autoload', True)
        self._is_optional = self._is_annotation_optional(self._annotation)
        self._is_list = self._is_annotation_list(self._annotation)
        self._type = self._extract_annotation_type(self._annotation)

    @property
    def name(self):
        return self._name

    @property
    def tag(self):
        return self._tag

    @property
    def annotation(self):
        return self._annotation

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    @property
    def autoload(self):
        return self._autoload

    @property
    def is_optional(self):
        return self._is_optional

    @property
    def is_list(self):
        return self._is_list

    def clone(self, **kwargs):
        params = {k[1:]: v for k, v in vars(self).items() if k in self._clone_attrs}
        params.update(kwargs)
        obj = type(self)(**params)
        return obj

    @staticmethod
    def _is_annotation_union(annotation: Any) -> bool:
        return annotation is not None and get_origin(annotation) is Union

    @staticmethod
    def _is_annotation_optional(annotation: Any) -> bool:
        return LottieAttribute._is_annotation_union(annotation) and type(None) in get_args(annotation)

    @staticmethod
    def _is_annotation_list(annotation: Any) -> bool:
        if LottieAttribute._is_annotation_optional(annotation):
            annotation = get_args(annotation)[0]
        if LottieAttribute._is_annotation_union(annotation):
            return False
        return annotation is list or (get_origin(annotation) is not None and issubclass(get_origin(annotation), List))

    @staticmethod
    def _extract_annotation_type(annotation: Any) -> type:
        if LottieAttribute._is_annotation_optional(annotation):
            annotation = get_args(annotation)[0]
        if LottieAttribute._is_annotation_list(annotation):
            annotation = get_args(annotation)[0]
        if LottieAttribute._is_annotation_union(annotation):
            annotation = get_args(annotation)
        return annotation

    def __repr__(self):
        return f"<LottieAttribute name='{self._name}' tag='{self._tag}' annotation={self._annotation})>"

    def __eq__(self, other):
        return all(getattr(self, attr) == getattr(other, attr) for attr in self._eq_attrs)
