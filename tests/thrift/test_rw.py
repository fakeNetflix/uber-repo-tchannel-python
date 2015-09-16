# Copyright (c) 2015 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pytest

from tchannel import thrift


@pytest.mark.parametrize('args, kwargs', [
    (['tests/data/idls/ThriftTest.thrift'], {}),
    (['server', 'tests/data/idls/ThriftTest.thrift'], {}),
    (['tests/data/idls/ThriftTest.thrift', 'server'], {}),
    ([], {'path': 'tests/data/idls/ThriftTest.thrift'}),

])
def test_load_backwards_compatibility(args, kwargs):
    """We initially required a ``service`` argument to always be provided."""
    assert thrift.load(*args, **kwargs).ThriftTest


def test_thriftrw_client_without_service_or_hostport_specified():
    client = thrift.load(
        'tests/data/idls/ThriftTest.thrift',
    )

    with pytest.raises(ValueError):
        client.ThriftTest.testVoid()


@pytest.mark.parametrize('hostport, service', [
    ('127.0.0.1:1234', None),
    ('127.0.0.1:1234', 'foo'),
    (None, 'foo'),
])
def test_thriftrw_client_with_service_or_hostport_specified(hostport, service):
    client = thrift.load(
        'tests/data/idls/ThriftTest.thrift',
        hostport=hostport,
        service=service,
    )

    assert client.ThriftTest.testVoid()
