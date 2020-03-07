#!/usr/bin/env python3

from pathlib import Path

#
# Process Canvas archives
#
def process_canvas_archive(prefix):
    for n in range(1,31):
        fn = "{}{:02d}".format(prefix,n)
        fs = list(Path("submissions").glob("*{}*".format(fn)))
        if len(fs) > 0:
            fs[0].rename("fixed/{}.zip".format(fn))
            if len(fs) > 1:
                fs[1].unlink()
                if len(fs) > 2:
                    fs[2].unlink()

process_canvas_archive("Group")
process_canvas_archive("Team")
