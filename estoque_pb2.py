# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: estoque.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'estoque.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\restoque.proto\"7\n\x0eProdutoRequest\x12\x12\n\nquantidade\x18\x01 \x01(\x05\x12\x11\n\tdescricao\x18\x02 \x01(\t\"\x17\n\tProdutoId\x12\n\n\x02id\x18\x01 \x01(\x05\"9\n\x17\x41lteraQuantidadeRequest\x12\x0f\n\x07prod_id\x18\x01 \x01(\x05\x12\r\n\x05valor\x18\x02 \x01(\x05\"\x18\n\x06Status\x12\x0e\n\x06status\x18\x01 \x01(\x05\"<\n\x07Produto\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tdescricao\x18\x02 \x01(\t\x12\x12\n\nquantidade\x18\x03 \x01(\x05\"-\n\x0fListaDeProdutos\x12\x1a\n\x08produtos\x18\x01 \x03(\x0b\x32\x08.Produto\"\x0e\n\x0c\x45mptyRequest2\xdb\x01\n\x0e\x45stoqueService\x12.\n\x0f\x41\x64icionaProduto\x12\x0f.ProdutoRequest\x1a\n.ProdutoId\x12>\n\x19\x41lteraQuantidadeDeProduto\x12\x18.AlteraQuantidadeRequest\x1a\x07.Status\x12\x30\n\rListaProdutos\x12\r.EmptyRequest\x1a\x10.ListaDeProdutos\x12\'\n\rFimDaExecucao\x12\r.EmptyRequest\x1a\x07.Statusb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'estoque_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUTOREQUEST']._serialized_start=17
  _globals['_PRODUTOREQUEST']._serialized_end=72
  _globals['_PRODUTOID']._serialized_start=74
  _globals['_PRODUTOID']._serialized_end=97
  _globals['_ALTERAQUANTIDADEREQUEST']._serialized_start=99
  _globals['_ALTERAQUANTIDADEREQUEST']._serialized_end=156
  _globals['_STATUS']._serialized_start=158
  _globals['_STATUS']._serialized_end=182
  _globals['_PRODUTO']._serialized_start=184
  _globals['_PRODUTO']._serialized_end=244
  _globals['_LISTADEPRODUTOS']._serialized_start=246
  _globals['_LISTADEPRODUTOS']._serialized_end=291
  _globals['_EMPTYREQUEST']._serialized_start=293
  _globals['_EMPTYREQUEST']._serialized_end=307
  _globals['_ESTOQUESERVICE']._serialized_start=310
  _globals['_ESTOQUESERVICE']._serialized_end=529
# @@protoc_insertion_point(module_scope)
