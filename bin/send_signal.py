from __future__ import print_function
from _signal import SIGINT
from os import environ
from time import sleep
from psutil import Process, NoSuchProcess


def _kill(pid, timeout):
    print(f"Kill Process [pid: {pid}, timeout: {timeout}]")
    try:
        process = Process(int(pid))
    except NoSuchProcess:
        return
    try:
        process.send_signal(SIGINT)
        sleep(int(timeout))
    except OSError:
        pass


if __name__ == '__main__':
    _pid = environ.get('PID', -1)
    _timeout = environ.get('TIMEOUT', 3)

    if _pid == -1:
        print("not found environment PID")
    else:
        _kill(_pid, _timeout)


