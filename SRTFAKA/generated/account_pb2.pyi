from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AccountRequestById(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class AccountRequestByUsername(_message.Message):
    __slots__ = ("username",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class CreateAccountRequest(_message.Message):
    __slots__ = ("firstname", "lastname", "username", "password", "email", "country", "address", "type")
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    firstname: str
    lastname: str
    username: str
    password: str
    email: str
    country: str
    address: str
    type: str
    def __init__(self, firstname: _Optional[str] = ..., lastname: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., email: _Optional[str] = ..., country: _Optional[str] = ..., address: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class UpdateAccountRequest(_message.Message):
    __slots__ = ("userId", "firstname", "lastname", "username", "password", "email", "country", "address", "type")
    USERID_FIELD_NUMBER: _ClassVar[int]
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    userId: str
    firstname: str
    lastname: str
    username: str
    password: str
    email: str
    country: str
    address: str
    type: str
    def __init__(self, userId: _Optional[str] = ..., firstname: _Optional[str] = ..., lastname: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., email: _Optional[str] = ..., country: _Optional[str] = ..., address: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class AccountResponse(_message.Message):
    __slots__ = ("userId", "firstname", "lastname", "username", "password", "email", "country", "address", "type")
    USERID_FIELD_NUMBER: _ClassVar[int]
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    userId: str
    firstname: str
    lastname: str
    username: str
    password: str
    email: str
    country: str
    address: str
    type: str
    def __init__(self, userId: _Optional[str] = ..., firstname: _Optional[str] = ..., lastname: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., email: _Optional[str] = ..., country: _Optional[str] = ..., address: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
