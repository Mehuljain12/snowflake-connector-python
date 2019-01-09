#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2018 Snowflake Computing Inc. All right reserved.
#

from logging import getLogger

import pytest

from snowflake.connector.compat import (TO_UNICODE)
from snowflake.connector.connection import DefaultConverterClass
from snowflake.connector.converter_snowsql import SnowflakeConverterSnowSQL

logger = getLogger(__name__)

ConverterSnowSQL = SnowflakeConverterSnowSQL


def test_is_dst():
    """
    SNOW-6020: Failed to convert to local time during DST is being
    changed
    """
    # DST to non-DST
    convClass = DefaultConverterClass()
    conv = convClass()
    conv.set_parameter('TIMEZONE', 'America/Los_Angeles')

    col_meta = {
        'name': 'CREATED_ON',
        'type': 6,
        'length': None,
        'precision': None,
        'scale': 3,
        'nullable': True,
    }
    m = conv.to_python_method('TIMESTAMP_LTZ', col_meta)
    ret = m('1414890189.000')

    assert TO_UNICODE(ret) == u'2014-11-01 18:03:09-07:00', \
        'Timestamp during from DST to non-DST'

    # non-DST to DST
    col_meta = {
        'name': 'CREATED_ON',
        'type': 6,
        'length': None,
        'precision': None,
        'scale': 3,
        'nullable': True,
    }
    m = conv.to_python_method('TIMESTAMP_LTZ', col_meta)
    ret = m('1425780189.000')

    assert TO_UNICODE(ret) == u'2015-03-07 18:03:09-08:00', \
        'Timestamp during from non-DST to DST'


def test_more_timestamps():
    conv = ConverterSnowSQL()
    conv.set_parameter('TIMESTAMP_NTZ_OUTPUT_FORMAT',
                       'YYYY-MM-DD HH24:MI:SS.FF9')
    m = conv.to_python_method('TIMESTAMP_NTZ', {'scale': 9})
    ret = m('-2208943503.876543211')
    assert ret == '1900-01-01 12:34:56.123456789'


@pytest.mark.skipif(False, reason='Benchmark Date')
def test_benchmark_date_converter():
    conv = ConverterSnowSQL(support_negative_year=True)
    conv.set_parameter('DATE_OUTPUT_FORMAT', 'YY-MM-DD')
    m = conv.to_python_method('DATE', {'scale': 0})
    current_date_counter = 12345
    for _ in range(2000000):
        m(current_date_counter)


@pytest.mark.skipif(False, reason='Benchmark Date')
def test_benchmark_date_without_negative_converter():
    conv = ConverterSnowSQL(support_negative_year=False)
    conv.set_parameter('DATE_OUTPUT_FORMAT', 'YY-MM-DD')
    m = conv.to_python_method('DATE', {'scale': 0})
    current_date_counter = 12345
    for _ in range(2000000):
        m(current_date_counter)


@pytest.mark.skipif(False, reason='Benchmark Timestamp')
def test_benchmark_timestamp_converter():
    conv = ConverterSnowSQL(support_negative_year=True)
    conv.set_parameter('TIMESTAMP_NTZ_OUTPUT_FORMAT',
                       'YYYY-MM-DD HH24:MI:SS.FF9')
    m = conv.to_python_method('TIMESTAMP_NTZ', {'scale': 9})
    current_timestamp = '2208943503.876543211'
    for _ in range(2000000):
        m(current_timestamp)


@pytest.mark.skipif(False, reason='Benchmark Timestamp')
def test_benchmark_timestamp_without_negative_converter():
    conv = ConverterSnowSQL(support_negative_year=False)
    conv.set_parameter('TIMESTAMP_NTZ_OUTPUT_FORMAT',
                       'YYYY-MM-DD HH24:MI:SS.FF9')
    m = conv.to_python_method('TIMESTAMP_NTZ', {'scale': 9})
    current_timestamp = '2208943503.876543211'
    for _ in range(2000000):
        m(current_timestamp)
