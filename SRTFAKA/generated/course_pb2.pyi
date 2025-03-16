from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CourseData(_message.Message):
    __slots__ = ("id", "name", "details", "industry_id", "industry_name", "cert_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    INDUSTRY_ID_FIELD_NUMBER: _ClassVar[int]
    INDUSTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    CERT_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    details: str
    industry_id: int
    industry_name: str
    cert_id: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., details: _Optional[str] = ..., industry_id: _Optional[int] = ..., industry_name: _Optional[str] = ..., cert_id: _Optional[int] = ...) -> None: ...

class CourseList(_message.Message):
    __slots__ = ("courses",)
    COURSES_FIELD_NUMBER: _ClassVar[int]
    courses: _containers.RepeatedCompositeFieldContainer[CourseData]
    def __init__(self, courses: _Optional[_Iterable[_Union[CourseData, _Mapping]]] = ...) -> None: ...

class CourseId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
