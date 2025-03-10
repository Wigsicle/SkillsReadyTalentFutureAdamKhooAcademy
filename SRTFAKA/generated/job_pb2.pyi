from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobData(_message.Message):
    __slots__ = ("jobId", "name", "description", "monthlySalary", "startDate", "endDate", "availableSpotCount", "companyId", "employmentTypeId", "industryId", "companyName", "industryName")
    JOBID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MONTHLYSALARY_FIELD_NUMBER: _ClassVar[int]
    STARTDATE_FIELD_NUMBER: _ClassVar[int]
    ENDDATE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLESPOTCOUNT_FIELD_NUMBER: _ClassVar[int]
    COMPANYID_FIELD_NUMBER: _ClassVar[int]
    EMPLOYMENTTYPEID_FIELD_NUMBER: _ClassVar[int]
    INDUSTRYID_FIELD_NUMBER: _ClassVar[int]
    COMPANYNAME_FIELD_NUMBER: _ClassVar[int]
    INDUSTRYNAME_FIELD_NUMBER: _ClassVar[int]
    jobId: int
    name: str
    description: str
    monthlySalary: int
    startDate: str
    endDate: str
    availableSpotCount: int
    companyId: int
    employmentTypeId: int
    industryId: int
    companyName: str
    industryName: str
    def __init__(self, jobId: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., monthlySalary: _Optional[int] = ..., startDate: _Optional[str] = ..., endDate: _Optional[str] = ..., availableSpotCount: _Optional[int] = ..., companyId: _Optional[int] = ..., employmentTypeId: _Optional[int] = ..., industryId: _Optional[int] = ..., companyName: _Optional[str] = ..., industryName: _Optional[str] = ...) -> None: ...

class JobList(_message.Message):
    __slots__ = ("jobs",)
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[JobData]
    def __init__(self, jobs: _Optional[_Iterable[_Union[JobData, _Mapping]]] = ...) -> None: ...

class JobId(_message.Message):
    __slots__ = ("jobId",)
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: int
    def __init__(self, jobId: _Optional[int] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ApplicationData(_message.Message):
    __slots__ = ("applicationId", "jobId", "jobName", "companyId", "appliedOn", "resumeLink", "additionalInfo", "industryId")
    APPLICATIONID_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    JOBNAME_FIELD_NUMBER: _ClassVar[int]
    COMPANYID_FIELD_NUMBER: _ClassVar[int]
    APPLIEDON_FIELD_NUMBER: _ClassVar[int]
    RESUMELINK_FIELD_NUMBER: _ClassVar[int]
    ADDITIONALINFO_FIELD_NUMBER: _ClassVar[int]
    INDUSTRYID_FIELD_NUMBER: _ClassVar[int]
    applicationId: int
    jobId: int
    jobName: str
    companyId: int
    appliedOn: str
    resumeLink: str
    additionalInfo: str
    industryId: int
    def __init__(self, applicationId: _Optional[int] = ..., jobId: _Optional[int] = ..., jobName: _Optional[str] = ..., companyId: _Optional[int] = ..., appliedOn: _Optional[str] = ..., resumeLink: _Optional[str] = ..., additionalInfo: _Optional[str] = ..., industryId: _Optional[int] = ...) -> None: ...

class ApplicationList(_message.Message):
    __slots__ = ("applications",)
    APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    applications: _containers.RepeatedCompositeFieldContainer[ApplicationData]
    def __init__(self, applications: _Optional[_Iterable[_Union[ApplicationData, _Mapping]]] = ...) -> None: ...

class ApplicationId(_message.Message):
    __slots__ = ("applicationId",)
    APPLICATIONID_FIELD_NUMBER: _ClassVar[int]
    applicationId: int
    def __init__(self, applicationId: _Optional[int] = ...) -> None: ...

class UserId(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: int
    def __init__(self, userId: _Optional[int] = ...) -> None: ...
