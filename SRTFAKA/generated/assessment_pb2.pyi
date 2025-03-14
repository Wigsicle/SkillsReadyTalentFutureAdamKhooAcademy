from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AssessmentData(_message.Message):
    __slots__ = ("name", "courseId", "assessmentId", "total_marks")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COURSEID_FIELD_NUMBER: _ClassVar[int]
    ASSESSMENTID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MARKS_FIELD_NUMBER: _ClassVar[int]
    name: str
    courseId: int
    assessmentId: int
    total_marks: float
    def __init__(self, name: _Optional[str] = ..., courseId: _Optional[int] = ..., assessmentId: _Optional[int] = ..., total_marks: _Optional[float] = ...) -> None: ...

class AssessmentList(_message.Message):
    __slots__ = ("assessments",)
    ASSESSMENTS_FIELD_NUMBER: _ClassVar[int]
    assessments: _containers.RepeatedCompositeFieldContainer[AssessmentData]
    def __init__(self, assessments: _Optional[_Iterable[_Union[AssessmentData, _Mapping]]] = ...) -> None: ...

class AssessmentId(_message.Message):
    __slots__ = ("assessmentId",)
    ASSESSMENTID_FIELD_NUMBER: _ClassVar[int]
    assessmentId: int
    def __init__(self, assessmentId: _Optional[int] = ...) -> None: ...
