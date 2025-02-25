from checkhealth.check_req import *

def init():
    if check_root():
        print ("[+] Root access enabled!")
    else:
        exit ("[-] Root access disabled! App won't start correctly, exiting..")
    
    if check_os():
        print ("[+] Detected Linux system!")
    else:
        exit ("[-] Non-Linux system detected! Due to unexpected behaviour app won't start")