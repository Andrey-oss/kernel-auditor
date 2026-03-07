'''
Module for checking system requirements for the project
Note: You can turn off it by editing settings.json file
If you wish to run it without root access, you won't be able to change anything!
'''

import sys
from checkhealth.check_req import check_root, check_os

def init_hc():
    '''Init system checks'''

    if check_root():
        print ("[+] Root access enabled!")
    else:
        sys.exit ("[-] Root access disabled! App won't start correctly, exiting..")

    if check_os():
        print ("[+] Detected Linux system!")
    else:
        sys.exit ("[-] Non-Linux system detected! Due to unexpected behaviour app won't start")
