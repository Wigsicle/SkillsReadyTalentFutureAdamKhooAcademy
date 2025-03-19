from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateData(_message.Message):
    __slots__ = ("id", "name", "courseId", "yearsValid", "description", "additionalInfo")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COURSEID_FIELD_NUMBER: _ClassVar[int]
    YEARSVALID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ADDITIONALINFO_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    courseId: int
    yearsValid: int
    description: str
    additionalInfo: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., courseId: _Optional[int] = ..., yearsValid: _Optional[int] = ..., description: _Optional[str] = ..., additionalInfo: _Optional[str] = ...) -> None: ...

class UserCertificateData(_message.Message):
    __slots__ = ("id", "userId", "certId", "issuedOn", "expiresOn", "additionalInfo")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    CERTID_FIELD_NUMBER: _ClassVar[int]
    ISSUEDON_FIELD_NUMBER: _ClassVar[int]
    EXPIRESON_FIELD_NUMBER: _ClassVar[int]
    ADDITIONALINFO_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    certId: int
    issuedOn: _timestamp_pb2.Timestamp
    expiresOn: _timestamp_pb2.Timestamp
    additionalInfo: str
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., certId: _Optional[int] = ..., issuedOn: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expiresOn: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., additionalInfo: _Optional[str] = ...) -> None: ...

class UserCertificateList(_message.Message):
    __slots__ = ("userCertificates",)
    USERCERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    userCertificates: _containers.RepeatedCompositeFieldContainer[UserCertificateData]
    def __init__(self, userCertificates: _Optional[_Iterable[_Union[UserCertificateData, _Mapping]]] = ...) -> None: ...

class UserId(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...
