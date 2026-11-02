"""Đóng gói source thành 10 file assets/d0..d9.bin (gzip JSON) như bản demo gốc.
Chạy: python3 tools/pack.py <thư mục source> <thư mục site>"""
import sys, os, json, gzip, shutil
src, site = sys.argv[1], sys.argv[2]
B = {'css': open(os.path.join(src, 'css.css'), encoding='utf-8').read()}
for k in ['qrcode', 'core', 'customer', 'merchant', 'admin']:
    B[k] = open(os.path.join(src, k + '.js'), encoding='utf-8').read()
data = gzip.compress(json.dumps(B, ensure_ascii=False).encode('utf-8'), 9)
os.makedirs(os.path.join(site, 'assets'), exist_ok=True)
n = 10; size = -(-len(data) // n)
for i in range(n):
    open(os.path.join(site, 'assets', f'd{i}.bin'), 'wb').write(data[i*size:(i+1)*size])
print('bundle bytes', len(data))
