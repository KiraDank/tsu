import attr
from pathlib import Path

from . import consts
from .defs import is_other_user


@attr.s(auto_attribs=True)
class GetShell:
    shell: str
    user: str
    c_uid: int

    def get(self):
        root_shell = consts.SYS_SHELL
        USER_SHELL = Path(Path.home(), ".termux/shell")
        BASH_SHELL = Path(consts.TERMUX_PREFIX, "bin/bash")

        shell = self.shell
        # Others user cannot access Termux environment
        if is_other_user(self.user, self.c_uid):
            shell = "system"

        # The Android system shell.
        if shell == "system":
            root_shell = consts.SYS_SHELL
        # Check if user has set a login shell
        elif USER_SHELL.exists():
            root_shell = str(USER_SHELL.resolve())
        # Or at least installed bash
        elif BASH_SHELL.exists():
            root_shell = str(BASH_SHELL)
        return root_shell
