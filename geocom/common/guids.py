# coding: utf-8

#  Copyright (c) 2019 | Geocom Informatik AG, Burgdorf, Switzerland | MIT License

"""
This module contains the :class:`Guid` class, which inherits from Pythons built-in ``UUID`` class.
It helps validating existing GUIDs (e.g. GlobalID's) and can generate new ones. It also helps formatting the GUID
for use in SQL queries.
"""

import uuid as _uuid


class Guid(_uuid.UUID):
    """
    Takes a UUID-like string or object as input and validates it. Can also be used to generate a new GUID.
    The `Guid` class inherits from the Python built-in UUID.

    :param value:               The value to parse as a GUID. Must be set if *allow_new* is ``True``.
    :param allow_new:           If set to ``True`` and *value* is ``None``, a new GUID will be generated.
                                The default is ``False``, which means that an exception will be raised if
                                *value* is not set.
    :raise geocom.tools.Guid.MissingGuidError:
                                This exception is raised when *allow_new* is ``False`` and *value* is ``None``.
    :raise geocom.tools.Guid.BadGuidError:
                                This exception is raised when *value* cannot be parsed to a GUID.

    Examples:

        >>> Guid(allow_new=True)
        Guid('459b46ce-6370-48ae-b3cc-220026d49ec2')
        >>> guid = Guid('{459b46ce-6370-48ae-b3cc-220026d49ec2}')
        >>> str(guid)  # this returns the GUID for Esri SQL expressions
        '{459B46CE-6370-48AE-B3CC-220026D49EC2}'
    """

    class MissingGuidError(TypeError):
        """
        This exception is raised when ``Guid`` is initialized without a *value*, while *allow_new* is ``False``,
        which is the default. Either set a *value* or set *allow_new* to ``True`` to prevent this error.
        """
        pass

    class BadGuidError(ValueError):
        """
        This exception is raised when the GUID string cannot be successfully parsed to a valid UUID-like object.
        """
        pass

    def __init__(self, value=None, allow_new: bool = False):
        try:
            if value is None:
                # create random UUID value (https://support.esri.com/en/technical-article/000011677)
                super().__init__(_uuid.uuid4().hex if allow_new else None)
            else:
                # value has been specified: try to parse it
                super().__init__(value.hex if isinstance(value, _uuid.UUID) else value)
        except (TypeError, ValueError, AttributeError):
            if not value and allow_new is False:
                raise Guid.MissingGuidError(f'{Guid.__name__} must be initialized with a value when allow_new=False')
            raise Guid.BadGuidError(f'{value!r} cannot be parsed to a valid {Guid.__name__}')

    def __eq__(self, other):
        if not isinstance(other, Guid):
            try:
                other = Guid(other)
            except (Guid.BadGuidError, Guid.MissingGuidError):
                return False
        return repr(other) == repr(self)

    def __repr__(self):
        """ Returns the representation of the current GUID. """
        return f'{Guid.__name__}({super().__str__()!r})'

    def __str__(self):
        """ Returns a GUID string wrapped in curly braces, ready to be used in ArcGIS SQL queries, for example. """
        return f'{{{super().__str__().upper()}}}'
