from streamer import (dll, t_streamer)
from typing import List
import ctypes

SUCCESS_ERROR_CODE = 0

def runai_start() -> t_streamer:
    streamer = t_streamer(0)
    error_code = dll.fn_runai_start(ctypes.byref(streamer))
    if error_code != SUCCESS_ERROR_CODE:
        raise Exception(
                f"Could not open streamer in libstreamer due to: {runai_response_str(error_code)}"
            )
    return streamer


def runai_end(streamer: t_streamer) -> None:
    return dll.fn_runai_end(streamer)


def runai_request(
    streamer: t_streamer,
    path: str,
    offset: int,
    bytesize: int,
    dst: memoryview,
    num_sizes: int,
    internal_sizes: List[int],
) -> None:
    error_code = dll.fn_runai_request(
        streamer,
        path.encode("utf-8"),
        offset,
        bytesize,
        dst,
        num_sizes,
        (ctypes.c_uint64 * num_sizes)(*internal_sizes),
    )
    if error_code != SUCCESS_ERROR_CODE:
        raise Exception(
                f"Could not send runai_request to libstreamer due to: {runai_response_str(error_code)}"
            )


def runai_response(streamer: t_streamer) -> int:
    value = ctypes.c_uint32()
    error_code = dll.fn_runai_response(streamer, ctypes.byref(value))
    if error_code != SUCCESS_ERROR_CODE:
        raise Exception(
                f"Could not receive runai_response from libstreamer due to: {runai_response_str(error_code)}"
            )
    return value.value


def runai_response_str(response_code: int) -> str:
    return dll.fn_runai_response_str(response_code)
