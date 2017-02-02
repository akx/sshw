from collections import defaultdict

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
    writes = defaultdict(list)

    def mock_spawn_or_exec(*args):
        return 0

    def mock_write(fd, text):
        writes[fd].append(text)

    monkeypatch.setattr(sshw, 'color_interface', ci)
    monkeypatch.setattr(sshw.os, 'spawnvp', mock_spawn_or_exec)
    monkeypatch.setattr(sshw.os, 'execvp', mock_spawn_or_exec)
    monkeypatch.setattr(sshw.os, 'write', mock_write)
    monkeypatch.expected_colors = ci.expected_colors
    monkeypatch.writes = writes
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


def test_iterm_chrome(p):
    p.setattr(sshw, 'color_interface', sshw.ITermColorInterface())
    sshw.color_interface.set_chrome_color((80, 80, 80))
    assert all(b'255' in write for write in p.writes[1])  # should be bright white
