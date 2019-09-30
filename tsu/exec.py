# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import subprocess
import re

from pathlib import Path
from . import consts

from conlog import Conlog


class TsuExec:
    @Conlog.fn
    def ver_cmp(self, console, su, shell, env=None):
        name = su.name
        su_path = su.lpath()
        checkver = [su_path] + su.veropt
        if su.multipath:
            print(
                "SuperSU is abandonware. Consider upgrading your SuperUser Application."
            )
            return
        try:
            ver = subprocess.check_output(checkver).decode("utf-8")
            console.debug(r" {name=} {ver=}")
            if su.verstring in ver:
                argv = [su.argmap["shell"], shell]
                init = su.argmap.get("init", False)
                if init:
                    argv = [init, *argv]

                console.debug("Calling {name=} with {argv=}")
                linux_execve(su_path, argv)
                return True
            else:
                return "VERERR"
        except FileNotFoundError:
            return False
        except PermissionError:
            return False


def linux_execve(cmd, args, env=None):
    exec = [cmd] + args
    subprocess.run(exec, env=env)
