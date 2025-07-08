"""Utilities methods"""

import os
import shutil

def copyfile(src, dst):
    """
    Copy a single file from src to dst.
    If src and dst are actually the same file (e.g. different paths mount to the same inode), swallow the error and do nothing.
    """
    # If the destination already exists and is the same file, skip straight away
    try:
        if os.path.exists(dst) and os.path.samefile(src, dst):
            return
    except (AttributeError, OSError):
        # samefile may not be supported on all platforms—ignore and try copying
        pass

    try:
        shutil.copyfile(src, dst)
    except shutil.SameFileError:
        # src and dst refer to the same file; nothing to do
        return