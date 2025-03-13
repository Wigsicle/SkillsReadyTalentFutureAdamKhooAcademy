from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateData(_message.Message):
    __slots__ = ("id", "name", "courseId", "validityPeriod", "description", "additionalInfo")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COURSEID_FIELD_NUMBER: _ClassVar[int]
    VALIDITYPERIOD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ADDITIONALINFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    courseId: str
    validityPeriod: str
    description: str
    additionalInfo: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., courseId: _Optional[str] = ..., validityPeriod: _Optional[str] = ..., description: _Optional[str] = ..., additionalInfo: _Optional[str] = ...) -> None: ...

class UserCertificateData(_message.Message):
    __slots__ = ("id", "userId", "certificateId", "issuedOn", "expiresOn", "additionalInfo")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATEID_FIELD_NUMBER: _ClassVar[int]
    ISSUEDON_FIELD_NUMBER: _ClassVar[int]
    EXPIRESON_FIELD_NUMBER: _ClassVar[int]
    ADDITIONALINFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    userId: str
    certificateId: str
    issuedOn: str
    expiresOn: str
    additionalInfo: str
    def __init__(self, id: _Optional[str] = ..., userId: _Optional[str] = ..., certificateId: _Optional[str] = ..., issuedOn: _Optional[str] = ..., expiresOn: _Optional[str] = ..., additionalInfo: _Optional[str] = ...) -> None: ...

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
