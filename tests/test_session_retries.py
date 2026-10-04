import io
import pickle

import pytest
from urllib3.util.retry import Retry

import requests
from requests.adapters import BaseAdapter
from requests.sessions import _SessionRetry
from tests.testserver.server import Server, consume_socket_content


def status_server(*statuses, retry_after=None):
    """Serve one response per connection, with the given status codes in order.

    The server stops after ``len(statuses)`` requests, so an unexpected extra
    retry fails with a connection error.
    """
    codes = iter(statuses)

    def handler(sock):
        request = consume_socket_content(sock, timeout=0.5)
        status = next(codes)
        headers = b"Content-Length: 0\r\nConnection: close\r\n"
        if retry_after is not None:
            headers += b"Retry-After: %d\r\n" % retry_after
        sock.send(b"HTTP/1.1 %d X\r\n%s\r\n" % (status, headers))
        return request

    return Server(handler, requests_to_handle=len(statuses))


def test_retries_default_is_none():
    assert requests.Session().retries is None


def test_no_retries_by_default():
    server = status_server(503)
    with server as (host, port):
        r = requests.Session().get(f"http://{host}:{port}/")
    assert r.status_code == 503
    assert len(server.handler_results) == 1


def test_retries_until_success():
    server = status_server(503, 200)
    with server as (host, port):
        s = requests.Session()
        s.retries = 3
        r = s.get(f"http://{host}:{port}/")
    assert r.status_code == 200
    assert len(server.handler_results) == 2


def test_returns_last_response_when_retries_exhausted():
    server = status_server(503, 502, 500)
    with server as (host, port):
        s = requests.Session()
        s.retries = 2
        r = s.get(f"http://{host}:{port}/")
    assert r.status_code == 500
    assert len(server.handler_results) == 3


def test_status_not_in_forcelist_is_not_retried():
    server = status_server(404)
    with server as (host, port):
        s = requests.Session()
        s.retries = 3
        r = s.get(f"http://{host}:{port}/")
    assert r.status_code == 404


def test_post_is_not_retried():
    server = status_server(503)
    with server as (host, port):
        s = requests.Session()
        s.retries = 3
        r = s.post(f"http://{host}:{port}/", data=b"x")
    assert r.status_code == 503
    assert len(server.handler_results) == 1


def test_file_body_is_resent_on_retry():
    server = status_server(503, 200)
    with server as (host, port):
        s = requests.Session()
        s.retries = 1
        r = s.put(f"http://{host}:{port}/", data=io.BytesIO(b"payload"))
    assert r.status_code == 200
    assert all(req.endswith(b"payload") for req in server.handler_results)


def test_generator_body_is_not_retried():
    server = status_server(503)
    with server as (host, port):
        s = requests.Session()
        s.retries = 3
        r = s.put(f"http://{host}:{port}/", data=iter([b"a", b"b"]))
    assert r.status_code == 503
    assert len(server.handler_results) == 1


def test_retry_object_is_used_as_is():
    server = status_server(418, 200)
    with server as (host, port):
        s = requests.Session()
        s.retries = Retry(total=1, status_forcelist=[418])
        r = s.get(f"http://{host}:{port}/")
    assert r.status_code == 200


def test_session_retries_override_adapter_max_retries():
    server = status_server(503, 200)
    with server as (host, port):
        s = requests.Session()
        s.mount("http://", requests.adapters.HTTPAdapter(max_retries=0))
        s.retries = 1
        r = s.get(f"http://{host}:{port}/")
    assert r.status_code == 200


def test_retries_not_passed_to_other_adapters():
    class Adapter(BaseAdapter):
        def send(self, request, **kwargs):
            assert "retries" not in kwargs
            r = requests.Response()
            r.status_code = 200
            r.request = request
            r.raw = io.BytesIO(b"")
            return r

        def close(self):
            pass

    s = requests.Session()
    s.mount("mock://", Adapter())
    s.retries = 3
    assert s.get("mock://host/").status_code == 200


def test_retries_not_passed_to_adapters_overriding_send():
    class OldAdapter(requests.adapters.HTTPAdapter):
        def send(
            self,
            request,
            stream=False,
            timeout=None,
            verify=True,
            cert=None,
            proxies=None,
        ):
            return super().send(request, stream, timeout, verify, cert, proxies)

    server = status_server(503)
    with server as (host, port):
        s = requests.Session()
        s.mount("http://", OldAdapter())
        s.retries = 3
        r = s.get(f"http://{host}:{port}/")
    assert r.status_code == 503


@pytest.mark.parametrize(
    "value, expected",
    (("5", 5), ("60", 60), ("3600", 60)),
)
def test_retry_after_is_capped(value, expected):
    assert _SessionRetry(total=1).parse_retry_after(value) == expected


def test_retries_pickling():
    s = requests.Session()
    s.retries = 2
    assert pickle.loads(pickle.dumps(s)).retries == 2

    # Sessions pickled before ``retries`` existed have no such state.
    state = s.__getstate__()
    del state["retries"]
    old = requests.Session.__new__(requests.Session)
    old.__setstate__(state)
    assert old.retries is None
