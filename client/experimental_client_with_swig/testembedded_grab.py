#!/usr/bin/env python3

import pm3
from output_grabber import OutputGrabber

out = OutputGrabber()
p=pm3.pm3()
print("Device:", p.name)
with out:
    p.console("hf search")
for line in out.capturedtext.split('\n'):
    if "UID" in line:
        print(line)