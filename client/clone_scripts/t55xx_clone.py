# import pm3
# from output_grabber import OutputGrabber
# import re


# out = OutputGrabber()
# p=pm3.pm3()

# password = None
# otp = None
# fp = None

# print("Device:", p.name)
# # DETECT PHASE
# with out:
#     p.console("lf t55xx detect")

# with open("debug.txt", "a") as f:
#     f.writelines("DETECT PHASE:\n")
#     for line in out.capturedtext.split('\n'):
#         if "Chip type" in line:
#             print(line)
#             f.writelines(line+"\n")
#         elif "Password set" in line:
#             if "Yes" in line:
#                 print("There is a password")
#                 password = True
#                 f.writelines(line+": Password is set. \n")
#             else:
#                 print("There is no password")
#                 f.writelines(line+": Password is NOT set. \n")
#                 password = False
#     f.close()


# # INFO PHASE
# out = OutputGrabber()
# with out:
#     p.console("lf t55xx info")

# with open("debug.txt", "a") as f:
#     f.writelines("INFO PHASE:\n")
#     for line in out.capturedtext.split('\n'):
#         if "OTP" in line:
#             if "Yes" in line:
#                 print("There is an OTP")
#                 otp = True
#                 f.writelines(line+": OTP is set. \n")
#             else:
#                 print("There is no OTP")
#                 f.writelines(line+": OTP is NOT set. \n")
#                 otp = False

#         elif "Password mode" in line:
#             if "Yes" in line:
#                 print("There is a password")
#                 password = True
#                 f.writelines(line+": Password is set. \n")
#             else:
#                 print("There is no password")
#                 f.writelines(line+": Password is NOT set. \n")
#                 password = False
#     f.close()


# # DUMP PHASE
# if not password and not otp:
#     out = OutputGrabber()
#     with out:
#         p.console("lf t55xx dump")

#     with open("debug.txt", "a") as f:
#         f.writelines("DUMP PHASE:\n")
#         for line in out.capturedtext.split('\n'):
#             f.writelines(line+"\n")
#             if "binary file" in line:
#                 tmp = line.split("`")[1]
#                 match = re.search(r'lf-.*?\.bin', tmp)
#                 fp = match.group(0)
#                 print(fp)
#                 f.writelines(fp+": FILEPATH\n")

#         f.close()


# # CLONE PHASE
# if fp:
#     input("Press enter once second card has been loaded")
#     out = OutputGrabber()
#     with out:
#         p.console(f"lf t55xx restore -f {fp}")

#     with open("debug.txt", "a") as f:
#         f.writelines("CLONE PHASE:\n")
#         for line in out.capturedtext.split('\n'):
#             f.writelines(line+"\n")
#             if "Done" in line:
#                 print("Cloning Successful.")
#                 f.writelines("Cloning Successful.")
#         f.close()

import pm3
from output_grabber import OutputGrabber
import re

class T55xxHandler:
    def __init__(self, device_name):
        self.device = pm3.pm3()
        self.name = device_name
        self.password = None
        self.otp = None
        self.fp = None

    def print_and_log(self, message, file):
        print(message)
        file.write(message + "\n")

    def detect(self):
        out = OutputGrabber()
        with out:
            self.device.console("lf t55xx detect")
        with open("debug.txt", "a") as f:
            f.write("DETECT PHASE:\n")
            for line in out.capturedtext.split('\n'):
                if "Chip type" in line or "Password set" in line:
                    self.print_and_log(line, f)
                    if "Password set" in line:
                        self.password = "Yes" in line

    def info(self):
        out = OutputGrabber()
        with out:
            self.device.console("lf t55xx info")
        with open("debug.txt", "a") as f:
            f.write("INFO PHASE:\n")
            for line in out.capturedtext.split('\n'):
                if "OTP" in line or "Password mode" in line:
                    self.print_and_log(line, f)
                    if "OTP" in line:
                        self.otp = "Yes" in line
                    elif "Password mode" in line:
                        self.password = "Yes" in line

    def dump(self):
        if not self.password and not self.otp:
            out = OutputGrabber()
            with out:
                self.device.console("lf t55xx dump")
            with open("debug.txt", "a") as f:
                f.write("DUMP PHASE:\n")
                for line in out.capturedtext.split('\n'):
                    print(line + "\n")
                    f.write(line + "\n")
                    if "binary file" in line:
                        tmp = line.split("`")[1]
                        match = re.search(r'lf-.*?\.bin', tmp)
                        self.fp = match.group(0)
                        self.print_and_log(self.fp, f)

    def clone(self):
        if self.fp:
            input("Press enter once second card has been loaded\nNOTICE: Will wipe the second card's details")
            out = OutputGrabber()
            with out:
                self.device.console(f"lf t55xx wipe")
                print("Wiping card details")
            out = OutputGrabber()
            with out:
                self.device.console(f"lf t55xx restore -f {self.fp}")
            with open("debug.txt", "a") as f:
                f.write("CLONE PHASE:\n")
                for line in out.capturedtext.split('\n'):
                    f.write(line + "\n")
                    if "Done" in line:
                        self.print_and_log("Cloning Successful.", f)

if __name__ == "__main__":
    t55xx = T55xxHandler(device_name="Your Device Name")
    t55xx.detect()
    t55xx.info()
    t55xx.dump()
    t55xx.clone()

