from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CourseProgressData(_message.Message):
    __slots__ = ("cleared", "student_id", "course_id")
    CLEARED_FIELD_NUMBER: _ClassVar[int]
    STUDENT_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    cleared: bool
    student_id: int
    course_id: int
    def __init__(self, cleared: bool = ..., student_id: _Optional[int] = ..., course_id: _Optional[int] = ...) -> None: ...
