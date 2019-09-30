# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import os
import sys

import os
import pwd
import pprint
from pathlib import Path, PurePath


from docopt import docopt

from conlog import Conlog
from .exec import TsuExec

from .su_bin import magisk, losu, chsu
from .defs import EnvMap, GetShell
from . import consts

CUR_UID = os.getuid()


def cli():
    """
    tsu A su interface wrapper for Termux

    Usage: 
        tsu
        tsu [ -s SHELL ]  [-pe] [USER] 
        tsu --debug [ -s SHELL ]  [-pel] [USER]
        tsu -h | --help | --version 
        

    Options:
    -s <shell>   Use an alternate specified shell.
    -l           Start a login shell.
    -p           Prepend system binaries to PATH
    -e           Start with a fresh environment.
    --debug      Output debugging information to stderr.
    -h --help    Show this screen.
    --version    Show version.

    """

    args = docopt(cli.__doc__)

    ### Debug handler
    debug_enabled = False
    conlog = Conlog("__main__", Conlog.DEBUG, enabled=debug_enabled)
    tsu_exec = conlog.impl(TsuExec, Conlog.DEBUG, debug_enabled)

    if args["--debug"] == True:
        print(f"Called with user={CUR_UID} ")
        args_fmt = "".join(f"{k}:{v} " for k, v in args.items())
        print(args_fmt)
        debug_enabled = True
    ### Debug handler

    ### Setup Shell and Enviroment
    env_new = EnvMap(
        prepend=(args.get("-p")), clean=(args.get("-e")), usern=(args.get("USER"))
    )
    env_new.setShell(args.get("-s"), CUR_UID)
    env, shell = env_new.getEnv()

    # Check `su` binaries:
    su_bins = [magisk, losu, chsu]
    for su_bin in su_bins:
        try:
            tsu_exec.ver_cmp(su_bin, shell, env)
        except PermissionError:
            pass

    print("su binary not found.")
    print("Are you rooted? ")
