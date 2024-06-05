class ModelMetaclass(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        new_class._validators = {}
        new_class._root_validators = []
        for _, attr_value in namespace.items():
            if callable(attr_value):
                if getattr(attr_value, "is_validator", False):
                    field_names = getattr(attr_value, "field_names", ())
                    bound_method = classmethod(attr_value)
                    for field_name in field_names:
                        if field_name not in new_class._validators:
                            new_class._validators[field_name] = []
                        new_class._validators[field_name].append(bound_method)
                elif getattr(attr_value, "is_root_validator", False):
                    bound_method = classmethod(attr_value)
                    new_class._root_validators.append(bound_method)
        return new_class
