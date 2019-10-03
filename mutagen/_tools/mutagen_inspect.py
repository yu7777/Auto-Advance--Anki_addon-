# -*- coding: utf-8 -*-
# Copyright 2005 Joe Wreschnig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""Full tag list for any given file."""

from ._senf import print_, argv
from ._compat import text_type

from ._util import SignalHandler, OptionParser


_sig = SignalHandler()


def main(argv):
    from mutagen import File

    parser = OptionParser()
    parser.add_option("--no-flac", help="Compatibility; does nothing.")
    parser.add_option("--no-mp3", help="Compatibility; does nothing.")
    parser.add_option("--no-apev2", help="Compatibility; does nothing.")

    (options, args) = parser.parse_args(argv[1:])
    if not args:
        raise SystemExit(parser.print_help() or 1)

    for filename in args:
        print_("--", filename)
        try:
            print_("-", File(filename).pprint())
        except AttributeError:
            print_("- Unknown file type")
        except Exception as err:
            print_(text_type(err))
        print_("")


def entry_point():
    _sig.init()
    return main(argv)