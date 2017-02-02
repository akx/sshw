#!/usr/bin/env python3

import colorsys
import hashlib
import os
import re
import sys


def parse_color(color):
    if ',' in color:
        return [int(component) for component in color.split(',')][:3]
    if color.startswith('#'):
        return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
    raise ValueError('unable to parse color %s; try r,g,b or #FFFFFF' % color)


class ColorInterface:
    def set_bg_color(self, rgb):
        pass

    def restore_bg_color(self):
        self.set_bg_color(default_color)


class ITermColorInterface(ColorInterface):
    def set_bg_color(self, rgb):
        r, g, b = rgb
        os.write(1, b'\033]Ph%02x%02x%02x\033\\' % (r, g, b))


def find_hostmap_match(user_host):
    if not os.path.isfile(hostmap_file):
        return
    host = user_host.group(2)
    user_host = user_host.group(0)
    with open(hostmap_file) as hostmap_fp:
        for line in hostmap_fp:
            if line.startswith('#') or '=' not in line:
                continue
            m_host, color = [p.strip() for p in line.rsplit('=', 1)]
            if any((m == m_host or re.match(m_host, m)) for m in (host, user_host)):
                return parse_color(color)


color_interface_class = ColorInterface
if os.environ.get('TERM_PROGRAM') == 'iTerm.app':
    color_interface_class = ITermColorInterface
is_tty = bool(os.isatty(1))
default_color = parse_color(os.environ.get('SSHW_DEFAULT_BG') or '25,25,25')
hostmap_file = os.path.expanduser(os.path.expandvars(os.environ.get('SSHW_HOSTMAP') or '~/.sshw_hosts'))
color_interface = color_interface_class()

def main(argv):
    changed = False
    user_host = None

    # perform rudimentary parsing of the command line to find the user/host parameter
    for arg in argv[1:]:
        if arg == '--':  # after the double dash everything's the command; we've missed our shot
            break
        user_host = re.match(r'([a-z0-9]+@)?([0-9a-z.]+)', arg, re.I)
        if user_host:
            break



    if is_tty and user_host:
        rgb = find_hostmap_match(user_host)
        if not rgb:
            user, host = user_host.groups()
            host_hash = hashlib.sha1(host.encode('ascii')).digest()
            hue = host_hash[0] / 255.
            rgb = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.7, 0.2)]
        color_interface.set_bg_color(rgb)
        changed = True

    if changed:
        try:
            return os.spawnvp(os.P_WAIT, 'ssh', argv)
        except KeyboardInterrupt:
            pass
        finally:
            color_interface.restore_bg_color()
    else:
        # if the colors weren't changed at all, we can just exec --
        # no need to attempt to restore the color -- and save some
        # memory and process table space. (as if that's at a premium.)
        return os.execvp('ssh', argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
