import pytest

import sshw

class MockColorInterface(sshw.ColorInterface):
    def __init__(self):
        self.expected_colors = []

    def set_bg_color(self, rgb):
        expected_color = self.expected_colors.pop(0)
        assert tuple(rgb) == tuple(expected_color)


@pytest.fixture()
def p(monkeypatch):
    ci = MockColorInterface()

    def mock_spawn_or_exec(*args):
        return 0

    monkeypatch.setattr(sshw, 'color_interface', ci)
    monkeypatch.setattr(sshw.os, 'spawnvp', mock_spawn_or_exec)
    monkeypatch.setattr(sshw.os, 'execvp', mock_spawn_or_exec)
    monkeypatch.expected_colors = ci.expected_colors
    return monkeypatch


HOSTMAP_CONTENT = """
#.*=#ignored
foo.*=#FFFFFF
"""


def test_hostmap(p, tmpdir):
    hostmap_file = tmpdir.join('hostmap')
    hostmap_file.write_text(HOSTMAP_CONTENT, encoding='utf-8')
    p.setattr(sshw, 'hostmap_file', str(hostmap_file))
    p.expected_colors.append((255, 255, 255))
    p.expected_colors.append(sshw.default_color)
    sshw.main(['ssh', 'foo@quux'])


def test_auto_color(p, tmpdir):
    p.expected_colors.append((18, 15, 51))
    p.expected_colors.append(sshw.default_color)
    sshw.main(['ssh', 'foo@quux'])
