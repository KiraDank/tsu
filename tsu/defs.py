from dataclasses import dataclass
from pathlib import Path

import os
import attr
import typing

from functools import lru_cache
from pwd import getpwnam

from . import consts


@attr.s(auto_attribs=True)
class SuBinary:
    name: str
    path: str
    verstring: str
    veropt: list
    argmap: dict
    multipath: typing.List[str] = None

    def lpath(self):
        if not self.multipath:
            return Path(self.path)


class EnvMap:
    _ENV_CLEAN_BASE = {"ANDROID_DATA": "/data", "ANDROID_ROOT": "/system"}

    _ENV_CLEAN_BASE_COPY = ["EXTERNAL_STORAGE", "LANG", "TERM"]

    _ENV_CLEAN_OTHER = {"HOME": "/", "PATH": "/system/bin:/system/xbin"}

    def __init__(self, prepend=False, clean=False):
        self.prependpath = prepend
        self.cleanenv = clean
        self.uid = os.getuid()

    def getEnv(self):

        if is_other_user(self.user, self.c_uid):
            pass
        if self.cleanenv:
            return self.clean_root
        pass

    @classmethod
    def __merge_base(E):
        env_b = E._ENV_CLEAN_BASE
        env_bcp = {key: os.environ[key] for key in E._ENV_CLEAN_BASE_COPY}
        return {**env_b, **env_bcp}

    @property
    def unclean_other(self):
        env_copy = os.environ
        env_copy["PATH"]

    def add_to_path(self, env_path, prep_path):
        front = self.prependpath
        sep = os.pathsep
        new_path = (
            f"{prep_path}{sep}{env_path}" if front else f"{env_path}{sep}{prep_path}"
        )
        return new_path

    @property
    def clean_other(self):
        E = EnvMap
        environ = E.__merge_base()
        return {**environ, **E._ENV_CLEAN_OTHER}

    @property
    def clean_root(self):
        E = EnvMap
        environ = E.__merge_base()
        PREFIX = consts.TERMUX_PREFIX
        PATH = self.add_to_path(
            f"{PREFIX}/bin:${PREFIX}/bin/applets", consts.ANDROIDSYSTEM_PATHS
        )
        env_root = {
            "HOME": "data/data/com.termux/files/home",
            "PATH": PATH,
            "PREFIX": f"{PREFIX}",
            "TMPDIR": f"{PREFIX}/tmp",
        }
        environ = {**environ, **env_root}
        return environ


@lru_cache(maxsize=4)
def is_other_user(user_n, uid):
    if user_n == 0 :
        return False
    target_uid = getpwnam(user_n).pw_uid
    is_other = (target_uid == 0) or (target_uid == uid)
    return is_other
