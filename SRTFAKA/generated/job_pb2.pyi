from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobData(_message.Message):
    __slots__ = ("jobId", "name", "company", "description", "salary", "startDate", "endDate", "employmentType")
    JOBID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SALARY_FIELD_NUMBER: _ClassVar[int]
    STARTDATE_FIELD_NUMBER: _ClassVar[int]
    ENDDATE_FIELD_NUMBER: _ClassVar[int]
    EMPLOYMENTTYPE_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    name: str
    company: str
    description: str
    salary: int
    startDate: str
    endDate: str
    employmentType: str
    def __init__(self, jobId: _Optional[str] = ..., name: _Optional[str] = ..., company: _Optional[str] = ..., description: _Optional[str] = ..., salary: _Optional[int] = ..., startDate: _Optional[str] = ..., endDate: _Optional[str] = ..., employmentType: _Optional[str] = ...) -> None: ...

class JobList(_message.Message):
    __slots__ = ("jobs",)
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[JobData]
    def __init__(self, jobs: _Optional[_Iterable[_Union[JobData, _Mapping]]] = ...) -> None: ...

class JobId(_message.Message):
    __slots__ = ("jobId",)
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ApplicationData(_message.Message):
    __slots__ = ("applicationId", "jobId", "jobName", "company", "appliedOn", "resumeLink", "additionalInfo")
    APPLICATIONID_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    JOBNAME_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    APPLIEDON_FIELD_NUMBER: _ClassVar[int]
    RESUMELINK_FIELD_NUMBER: _ClassVar[int]
    ADDITIONALINFO_FIELD_NUMBER: _ClassVar[int]
    applicationId: str
    jobId: str
    jobName: str
    company: str
    appliedOn: str
    resumeLink: str
    additionalInfo: str
    def __init__(self, applicationId: _Optional[str] = ..., jobId: _Optional[str] = ..., jobName: _Optional[str] = ..., company: _Optional[str] = ..., appliedOn: _Optional[str] = ..., resumeLink: _Optional[str] = ..., additionalInfo: _Optional[str] = ...) -> None: ...

class ApplicationList(_message.Message):
    __slots__ = ("applications",)
    APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    applications: _containers.RepeatedCompositeFieldContainer[ApplicationData]
    def __init__(self, applications: _Optional[_Iterable[_Union[ApplicationData, _Mapping]]] = ...) -> None: ...

class ApplicationId(_message.Message):
    __slots__ = ("applicationId",)
    APPLICATIONID_FIELD_NUMBER: _ClassVar[int]
    applicationId: str
    def __init__(self, applicationId: _Optional[str] = ...) -> None: ...

class UserId(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...
