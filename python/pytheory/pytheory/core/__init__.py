import inspect
from collections import defaultdict


class var:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "S(%s)" % self.name


class UnifiedObject:
    atomic_types = {list, tuple, int, str, float, complex, bool, dict, var}

    @classmethod
    def convert(cls, x):
        if type(x) in UnifiedObject.atomic_types:
            return getattr(UnifiedObject, 'convert_' + type(x).__name__)(x)
        elif '__dict__' in dir(x):
            return UnifiedObject(type(x), [cls.convert(x.__dict__)])

    @classmethod
    def convert_list(cls, x):
        return UnifiedObject(type(x), [cls.convert(e) for e in x])

    @classmethod
    def convert_tuple(cls, x):
        return UnifiedObject(type(x), [cls.convert(e) for e in x])

    @classmethod
    def _convert_atomic(cls, x):
        return x

    @classmethod
    def convert_int(cls, x):
        return cls._convert_atomic(x)

    @classmethod
    def convert_str(cls, x):
        return cls._convert_atomic(x)

    @classmethod
    def convert_float(cls, x):
        return cls._convert_atomic(x)

    @classmethod
    def convert_complex(cls, x):
        return cls._convert_atomic(x)

    @classmethod
    def convert_bool(cls, x):
        return cls._convert_atomic(x)

    @classmethod
    def convert_symbol(cls, x):
        return cls._convert_atomic(x)

    @classmethod
    def convert_dict(cls, x):
        keys = sorted(x.keys(), key=lambda k: (type(k).__name__, repr(k)))
        return UnifiedObject(type(x), [cls.convert((key, x[key])) for key in keys])

    def __init__(self, head, args):
        self.head = head
        self.args = args

    def __repr__(self):
        return "[%s](%s)" % (repr(self.head), ",".join([repr(e) for e in self.args]))


class Matcher:
    def __init__(self):
        self.context = []

    def validate_context(self):
        d = defaultdict(list)
        for s, v in self.context:
            d[s.name].append(v)

        for name in d:
            values = d[name]
            for i in range(len(values)):
                for j in range(len(values)):
                    if i < j and not self._match(values[i], values[j]):
                        return False

        return True

    def match(self, a, b):
        self.context = []
        if type(a) is var:
            res = self._match(a, UnifiedObject.convert(b))
        else:
            res = self._match(UnifiedObject.convert(a), UnifiedObject.convert(b))

        return self.validate_context() and res

    def _match(self, a, b):
        if type(a) is var:
            self.context.append((a, b))
            return True

        if type(a) in UnifiedObject.atomic_types and type(b) in UnifiedObject.atomic_types:
            return type(a) == type(b) and a == b

        if type(a) is UnifiedObject and type(b) is UnifiedObject:
            if a.head == b.head and len(a.args) == len(b.args):
                for i, arg in enumerate(a.args):
                    if not self._match(arg, b.args[i]):
                        return False
                return True
            else:
                return False

        return False
