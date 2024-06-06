class ModelMetaclass(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)

        new_class._validators = {}
        new_class._root_validators = []

        for validator in cls._get_validators(namespace):
            field_names = getattr(validator, "field_names", ())
            bound_method = classmethod(validator)
            for field_name in field_names:
                if field_name not in new_class._validators:
                    new_class._validators[field_name] = []
                new_class._validators[field_name].append(bound_method)

        new_class._root_validators = [
            classmethod(root_validator)
            for root_validator in cls._get_root_validators(namespace)
        ]

        return new_class

    @classmethod
    def _get_validators(cls, namespace):
        return (
            item
            for item in cls._iterate_namespace(namespace)
            if getattr(item, "is_validator", False)
        )

    @classmethod
    def _get_root_validators(cls, namespace):
        return (
            item
            for item in cls._iterate_namespace(namespace)
            if getattr(item, "is_root_validator", False)
        )

    @staticmethod
    def _iterate_namespace(namespace):
        return namespace.values()
