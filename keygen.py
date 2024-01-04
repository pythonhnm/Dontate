from cryptography.hazmat.primitives.asymmetric import x25519
def genkeypair():
    private = x25519.X25519PrivateKey.generate()
    public = private.public_key()
    return public.public_bytes_raw()+private.private_bytes_raw()
print('[*] Creating a curve25519 key...')
key = genkeypair()
print('[+] Done!')
label = input('[?] Please input a label for this key:')
for i in ['?','*','/','\\','<','>']:
    if i in label or label == '':
        print("[!] ['?','*','/','\\','<','>'] can not in the label!")
        input()
        exit()
with open('./key/'+label+'.key','wb') as f:
    f.write(key)
print('[+] OK!')
input()
