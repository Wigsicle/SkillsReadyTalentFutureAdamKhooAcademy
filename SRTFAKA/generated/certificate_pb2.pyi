from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateData(_message.Message):
    __slots__ = ("name", "courseId", "certificateId")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COURSEID_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATEID_FIELD_NUMBER: _ClassVar[int]
    name: str
    courseId: str
    certificateId: str
    def __init__(self, name: _Optional[str] = ..., courseId: _Optional[str] = ..., certificateId: _Optional[str] = ...) -> None: ...

class CertificateList(_message.Message):
    __slots__ = ("certificates",)
    CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    certificates: _containers.RepeatedCompositeFieldContainer[CertificateData]
    def __init__(self, certificates: _Optional[_Iterable[_Union[CertificateData, _Mapping]]] = ...) -> None: ...

class CertificateId(_message.Message):
    __slots__ = ("certificateId",)
    CERTIFICATEID_FIELD_NUMBER: _ClassVar[int]
    certificateId: str
    def __init__(self, certificateId: _Optional[str] = ...) -> None: ...
