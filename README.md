# Requests

[![Version](https://img.shields.io/pypi/v/requests.svg?maxAge=86400)](https://pypi.org/project/requests/)
[![Supported Versions](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/requests)
[![Downloads](https://static.pepy.tech/badge/requests/month)](https://pepy.tech/project/requests)
[![Contributors](https://img.shields.io/github/contributors/psf/requests.svg)](https://github.com/psf/requests/graphs/contributors)
[![Documentation](https://readthedocs.org/projects/requests/badge/?version=latest)](https://requests.readthedocs.io)

**Requests** is a simple, yet elegant, HTTP library.

```python
>>> import requests
>>> r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"authenticated": true, ...'
>>> r.json()
{'authenticated': True, ...}
```

Requests allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your `PUT` & `POST` data — but nowadays, just use the `json` method!

Requests is one of the most downloaded Python packages today, pulling in around `300M downloads / week` — according to GitHub, Requests is currently [depended upon](https://github.com/psf/requests/network/dependents?package_id=UGFja2FnZS01NzA4OTExNg%3D%3D) by `4,000,000+` repositories.

## Installing Requests and Supported Versions

Requests is available on PyPI:

```console
$ python -m pip install requests
```

Requests officially supports Python 3.10+.

## Supported Features & Best–Practices

Requests is ready for the demands of building robust and reliable HTTP–speaking applications, for the needs of today.

- Keep-Alive & Connection Pooling
- International Domains and URLs
- Sessions with Cookie Persistence
- Browser-style TLS/SSL Verification
- Basic & Digest Authentication
- Familiar `dict`–like Cookies
- Automatic Content Decompression and Decoding
- Multi-part File Uploads
- SOCKS Proxy Support
- Connection Timeouts, with Session-wide Defaults
- Automatic Retries that honor `Retry-After`
- Streaming Downloads
- Automatic honoring of `.netrc`
- Chunked HTTP Requests

## Resilient Sessions

A `Session` can set a default timeout and retry policy for every request it sends:

```python
>>> import requests
>>> s = requests.Session()
>>> s.timeout = (3.05, 27)  # (connect, read) seconds, for every request
>>> s.retries = 3           # retry connection errors and 429/5xx responses
>>> r = s.get('https://api.example.com/items')
>>> if r.status_code == 429:  # still rate limited after all retries
...     print('Try again in', r.retry_after, 'seconds')
```

Retries apply only to idempotent methods, so a `POST` is never sent twice. They back off exponentially and wait for the server's `Retry-After` header, up to 60 seconds. Pass `timeout=(None, None)` to let a single request wait forever. See the [advanced usage docs](https://requests.readthedocs.io/en/latest/user/advanced/) for details.

## Cloning the repository

When cloning the Requests repository, you may need to add the `-c
fetch.fsck.badTimezone=ignore` flag to avoid an error about a bad commit timestamp (see
[this issue](https://github.com/psf/requests/issues/2690) for more background):

```shell
git clone -c fetch.fsck.badTimezone=ignore https://github.com/psf/requests.git
```

You can also apply this setting to your global Git config:

```shell
git config --global fetch.fsck.badTimezone ignore
```

---

[![Kenneth Reitz](https://raw.githubusercontent.com/psf/requests/main/ext/kr.png)](https://kennethreitz.org) [![Python Software Foundation](https://raw.githubusercontent.com/psf/requests/main/ext/psf.png)](https://www.python.org/psf)
