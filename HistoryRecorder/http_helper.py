import binascii
import json
import os
from http import client
import mimetypes
from http.client import HTTPResponse
from pathlib import Path
from typing import Tuple, TextIO, List


def get_filename(path: str) -> str:
    """Get file name from path"""
    return Path(path).name


def file_to_body(field_name: str, file_pointer: TextIO) -> Tuple[bytes, str]:
    """
    Encode file into multipart/form-data body
    """
    boundary = binascii.hexlify(os.urandom(16)).decode('ascii')

    filename = get_filename(file_pointer.name)

    body = (
        "--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"{field_name}\"; filename=\"{filename}\"\r\n"
        "Content-Type: {content_type}\r\n"
        "\r\n"
        "{file_content}\r\n"
        "--{boundary}--"
    ).format(
        boundary=boundary,
        field_name=field_name,
        filename=filename,
        content_type=get_content_type(filename),
        file_content=file_pointer.read()
    )

    content_type = f"multipart/form-data; boundary={boundary}"

    return body.encode('utf-8'), content_type


def post_file(
        host: str, path: str, field: str, file_pointer: TextIO
) -> HTTPResponse:
    body, content_type = file_to_body(field, file_pointer)
    h = client.HTTPConnection(host)
    h.putrequest('POST', path)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    response = h.getresponse()
    return response


def server_test(host: str) -> Tuple[bool, str]:
    """Send a HEAD request to the server to check if it responds"""
    try:
        h = client.HTTPConnection(host)
        h.putrequest('HEAD', '/')
        h.endheaders()
        h.send(b"")
        h.getresponse()
        return True, "Server is available"
    except Exception as e:
        print(e, e.__class__)
        return False, f"({e.__class__.__name__}) {e}"


def get_content_type(filename: str) -> str:
    """Get mime type based on file's name"""
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def post_records(host: str, path: str, records: List[dict]):
    body = json.dumps(records).encode('utf-8')
    content_type = "application/json"
    h = client.HTTPConnection(host)
    h.putrequest('POST', path)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    response = h.getresponse()
    return response
