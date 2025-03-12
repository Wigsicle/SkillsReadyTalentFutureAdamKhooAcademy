# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: account.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'account.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\raccount.proto\x12\x07\x61\x63\x63ount\"$\n\x12\x41\x63\x63ountRequestById\x12\x0e\n\x06userId\x18\x01 \x01(\t\",\n\x18\x41\x63\x63ountRequestByUsername\x12\x10\n\x08username\x18\x01 \x01(\t\"\xa6\x01\n\x14\x43reateAccountRequest\x12\x11\n\tfirstname\x18\x01 \x01(\t\x12\x10\n\x08lastname\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\r\n\x05\x65mail\x18\x05 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x06 \x01(\x05\x12\x0f\n\x07\x61\x64\x64ress\x18\x07 \x01(\t\x12\x14\n\x0cuser_type_id\x18\x08 \x01(\x05\"\xa3\x01\n\x14UpdateAccountRequest\x12\x0e\n\x06userId\x18\x01 \x01(\t\x12\x11\n\tfirstname\x18\x02 \x01(\t\x12\x10\n\x08lastname\x18\x03 \x01(\t\x12\x10\n\x08username\x18\x04 \x01(\t\x12\x10\n\x08password\x18\x05 \x01(\t\x12\r\n\x05\x65mail\x18\x06 \x01(\t\x12\x12\n\ncountry_id\x18\x07 \x01(\x05\x12\x0f\n\x07\x61\x64\x64ress\x18\x08 \x01(\t\"\xb4\x01\n\x0f\x41\x63\x63ountResponse\x12\x0e\n\x06userId\x18\x01 \x01(\t\x12\x11\n\tfirstname\x18\x02 \x01(\t\x12\x10\n\x08lastname\x18\x03 \x01(\t\x12\x10\n\x08username\x18\x04 \x01(\t\x12\x10\n\x08password\x18\x05 \x01(\t\x12\r\n\x05\x65mail\x18\x06 \x01(\t\x12\x12\n\ncountry_id\x18\x07 \x01(\x05\x12\x0f\n\x07\x61\x64\x64ress\x18\x08 \x01(\t\x12\x14\n\x0cuser_type_id\x18\t \x01(\x05\"1\n\x0e\x44\x65leteResponse\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t2\x8e\x03\n\x07\x41\x63\x63ount\x12I\n\x0eGetAccountById\x12\x1b.account.AccountRequestById\x1a\x18.account.AccountResponse\"\x00\x12U\n\x14GetAccountByUsername\x12!.account.AccountRequestByUsername\x1a\x18.account.AccountResponse\"\x00\x12J\n\rUpdateAccount\x12\x1d.account.UpdateAccountRequest\x1a\x18.account.AccountResponse\"\x00\x12J\n\rCreateAccount\x12\x1d.account.CreateAccountRequest\x1a\x18.account.AccountResponse\"\x00\x12I\n\rDeleteAccount\x12\x1d.account.UpdateAccountRequest\x1a\x17.account.DeleteResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'account_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ACCOUNTREQUESTBYID']._serialized_start=26
  _globals['_ACCOUNTREQUESTBYID']._serialized_end=62
  _globals['_ACCOUNTREQUESTBYUSERNAME']._serialized_start=64
  _globals['_ACCOUNTREQUESTBYUSERNAME']._serialized_end=108
  _globals['_CREATEACCOUNTREQUEST']._serialized_start=111
  _globals['_CREATEACCOUNTREQUEST']._serialized_end=277
  _globals['_UPDATEACCOUNTREQUEST']._serialized_start=280
  _globals['_UPDATEACCOUNTREQUEST']._serialized_end=443
  _globals['_ACCOUNTRESPONSE']._serialized_start=446
  _globals['_ACCOUNTRESPONSE']._serialized_end=626
  _globals['_DELETERESPONSE']._serialized_start=628
  _globals['_DELETERESPONSE']._serialized_end=677
  _globals['_ACCOUNT']._serialized_start=680
  _globals['_ACCOUNT']._serialized_end=1078
# @@protoc_insertion_point(module_scope)
