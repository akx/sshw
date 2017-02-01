import pytest

import sshw


@pytest.fixture()
def p(monkeypatch):

    expected_colors = []

    def mock_set_bg_color(rgb):
        expected_color = expected_colors.pop(0)
        assert tuple(rgb) == tuple(expected_color)

    def mock_spawn_or_exec(*args):
        return 0

    monkeypatch.setattr(sshw, 'set_bg_color', mock_set_bg_color)
    monkeypatch.setattr(sshw.os, 'spawnvp', mock_spawn_or_exec)
    monkeypatch.setattr(sshw.os, 'execvp', mock_spawn_or_exec)
    monkeypatch.expected_colors = expected_colors
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
