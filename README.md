# sshw

> :computer: Goodifying terminals for SSH!

`sshw` is a wrapper for `ssh` that automatically sets your terminal's
background color to something easily recognizable, so you know which
server you're about to hose.

![See it in action](https://github.com/akx/sshw/raw/gif/sshw.gif)

Support
-------

Currently `sshw` *only supports* [iTerm][iterm-ec]'s proprietary escape
codes.  Pull requests are more than welcome!

Installation
------------

* Clone the repository somewhere -- assuming `~/code`.
* Create an alias in your shell that makes `ssh` point to `sshw.py`.
  In `bash` and `fish`, `alias ssh=~/code/sshw.py` should do.
* You may also want to symlink `sshw.py` into your user `bin` directory
  or similar, if you have one: `ln -s ~/bin/sshw ~/code/sshw.py`.

You're done! The alias will kick in, `sshw` will parse your `ssh` command
line, configure your terminal and hand control to `ssh`.

Configuration
-------------

No configuration required! `sshw` will figure out a dark color for your
shell background automagically.

There are some environment variables `sshw` knows, though:

* `SSHW_DEFAULT_BG`: what color to return the terminal to after `ssh` quits.
  Currently there is no way of knowing what the original palette was before
  messing about with it, so this is used to restore the non-ssh-y color.
  This can be either an integer `rrr,ggg,bbb` triple or a web hex triplet like
  `#RRGGBB`.  Defaults to `25,25,25`.
* `SSHW_HOSTMAP`: the path to the SSHW hostmap file; defaults to `~/.sshw_hosts`.
  See below for more information about the hostmap.
* `SSHW_CHROME`: whether or not to set chrome (tab for iTerm) colors.  Defaults
  to yes; feel free to set to anything but "1", "true", or "yes" to disable this.

Hostmap
-------

In addition to the harmonious hues automatically determined from hostnames, you
can create a hostmap file, `~/.sshw_hosts` (or something else, see above).

The hostmap consists of key-value pairs (parsed sequentially; the first match
takes effect).  The "key" is a regexp that is matched against both the entire
`user@host` parameter and the `host` part. Lines starting with octothorpes (`#`)
are ignored.  If no match is found in the hostmap, the usual auto-color algorithm
is used.

```
# red background for all root
root@.*=#FF0000
# orange background for all production servers
.*production.*=#FFCC00
```

Development
-----------

Run tests with `py.test`.

[iterm-ec]: https://www.iterm2.com/documentation-escape-codes.html
