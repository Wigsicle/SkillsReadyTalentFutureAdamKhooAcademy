from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CourseData(_message.Message):
    __slots__ = ("name", "details", "industry_id", "cert_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    INDUSTRY_ID_FIELD_NUMBER: _ClassVar[int]
    CERT_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    details: str
    industry_id: int
    cert_id: int
    def __init__(self, name: _Optional[str] = ..., details: _Optional[str] = ..., industry_id: _Optional[int] = ..., cert_id: _Optional[int] = ...) -> None: ...

class CourseList(_message.Message):
    __slots__ = ("courses",)
    COURSES_FIELD_NUMBER: _ClassVar[int]
    courses: _containers.RepeatedCompositeFieldContainer[CourseData]
    def __init__(self, courses: _Optional[_Iterable[_Union[CourseData, _Mapping]]] = ...) -> None: ...

class CourseId(_message.Message):
    __slots__ = ("courseId",)
    COURSEID_FIELD_NUMBER: _ClassVar[int]
    courseId: str
    def __init__(self, courseId: _Optional[str] = ...) -> None: ...
