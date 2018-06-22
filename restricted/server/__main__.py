"""
Main server launcher
"""
import os
import sys
import fcntl
import logging
from pathlib import Path
from .server import Server

ADDR = Path('/tmp/restricted.socket')
PID_FILE = Path('/tmp/restricted.pid')


def check_sudo():
    """
    Exit the program if the process has no root premissions

    :raise SystemExit: if the user uid is not 0
    """
    if os.getuid() != 0:
        sys.exit('Error: must be run as root (uid 0)')


def main():
    """
    Main server launcher
    """
    logging.getLogger().setLevel(logging.INFO)
    check_sudo()
    with PID_FILE.open('w+') as fd:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(f'Could not lock {PID_FILE}, terminate the running instance of the server')
            sys.exit(2)
        try:
            Server(ADDR).main()
        except KeyboardInterrupt:
            pass
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            ADDR.unlink()
    PID_FILE.unlink()


if __name__ == '__main__':
    main()
