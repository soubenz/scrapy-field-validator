
class Type(Validator):
    """A validator accepting values that are instances of one or more given types.
    Attributes:
        - accept_types: A type or tuple of types that are valid.
        - reject_types: A type or tuple of types that are invalid.
    """

    accept_types = ()
    reject_types = ()

    def __init__(self, accept_types=None, reject_types=None):
        if accept_types is not None:
            self.accept_types = accept_types
        if reject_types is not None:
            self.reject_types = reject_types

    def validate(self, value, adapt=True):
        if not isinstance(value, self.accept_types) or isinstance(value, self.reject_types):
            self.error(value)
        return value

    @property
    def humanized_name(self):
        return self.name or _format_types(self.accept_types)


class Integer(Type):
    """
    A validator that accepts integers (:py:class:`numbers.Integral` instances)
    but not bool.
    """

    name = "integer"
    accept_types = numbers.Integral
    reject_types = bool




class Date(Type):
    """A validator that accepts :py:class:`datetime.date` values."""

    name = "date"
    accept_types = datetime.date


class Datetime(Type):
    """A validator that accepts :py:class:`datetime.datetime` values."""

    name = "datetime"
    accept_types = datetime.datetime


class Time(Type):
    """A validator that accepts :py:class:`datetime.time` values."""

    name = "time"
    accept_types = datetime.time



class String(Type):
    """A validator that accepts string values."""

    name = "string"
    accept_types = string_types

    def __init__(self, min_length=None, max_length=None):
        """Instantiate a String validator.
        :param min_length: If not None, strings shorter than ``min_length`` are
            invalid.
        :param max_length: If not None, strings longer than ``max_length`` are
            invalid.
        """
        super(String, self).__init__()
        self._min_length = min_length
        self._max_length = max_length

    def validate(self, value, adapt=True):
        super(String, self).validate(value)
        if self._min_length is not None and len(value) < self._min_length:
            raise ValidationError("must be at least %d characters long" %
                                  self._min_length, value)
        if self._max_length is not None and len(value) > self._max_length:
            raise ValidationError("must be at most %d characters long" %
                                  self._max_length, value)
        return value


