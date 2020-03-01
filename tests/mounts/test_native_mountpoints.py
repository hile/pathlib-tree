
from systematic_files.mounts import Mountpoints


def test_local_mountpoints_loading():
    """
    Test loading mountpoints from local system
    """
    mountpoints = mountpoints = Mountpoints()
    assert mountpoints.__loaded__ is False
    assert len(mountpoints) > 0
    assert mountpoints.__loaded__ is True
