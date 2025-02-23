from checkhealth.check_req import *

def init():
    if check_root():
        print ("[+] Root access enabled!")
    else:
        print ("[-] Root access disabled! Some functions won't work")
    
    if check_os():
        print ("[+] Detected Linux system!")
    else:
        exit ("[-] Non-Linux system detected! Due to unexpected behaviour app won't start")