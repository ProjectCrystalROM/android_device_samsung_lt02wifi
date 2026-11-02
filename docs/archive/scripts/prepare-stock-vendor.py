#!/usr/bin/env python3
from pathlib import Path
import hashlib, re, shutil, subprocess
base=Path('/home/airi/Tab3/cm11')
stock=Path('/home/airi/Tab3/stock-reference/full-system')
origin=base/'vendor/samsung/lt02wifi/lt02wifi-vendor-blobs.mk'
target=base/'vendor/samsung/lt02wifi-stockfull'
target.mkdir(parents=True,exist_ok=True)
pairs=re.findall(r'vendor/samsung/lt02wifi/proprietary/system/([^\s:]+):([^\s\\]+)',origin.read_text())
selected={}; missing=[]
for rel,dest in pairs:
 src=stock/rel
 if src.is_file(): selected[dest]=src
 else: missing.append((rel,dest))
# Extra components required by the stock graphics stack and stock power HAL.
for rel in ['lib/libmvmem.so','etc/powerhal.conf']:
 src=stock/rel
 if not src.is_file(): raise SystemExit('Missing essential stock file: '+str(src))
 selected['system/'+rel]=src
# Add stock library dependencies absent from both the stock selection and the
# previously built platform output. Dynamic dlopen dependencies require further review.
previous=base/'out-stockgpu/target/product/lt02wifi/system'
removed={dest for _,dest in missing}
seen=set(); added=[]; unresolved={}
while True:
 pending=[(d,p) for d,p in selected.items() if d not in seen]
 if not pending: break
 for dest,src in pending:
  seen.add(dest)
  with src.open('rb') as f:
   if f.read(4)!=b'\x7fELF': continue
  result=subprocess.run(['readelf','-d',str(src)],capture_output=True,text=True)
  for lib in re.findall(r'\(NEEDED\).*\[([^]]+)\]',result.stdout):
   out='system/lib/'+lib
   if out in selected or ('system/vendor/lib/'+lib) in selected or ('system/lib/egl/'+lib) in selected: continue
   existing=previous/'lib'/lib
   if existing.is_file() and out not in removed: continue
   candidate=stock/'lib'/lib
   if candidate.is_file(): selected[out]=candidate; added.append(out)
   else: unresolved.setdefault(lib,[]).append(dest)
lines=['# Generated from Samsung T210RUEU0COI1 stock firmware.','PRODUCT_COPY_FILES += \\']
for i,(dest,src) in enumerate(sorted(selected.items())):
 out=target/'proprietary'/dest
 out.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src,out)
 lines.append('    vendor/samsung/lt02wifi-stockfull/proprietary/%s:%s%s' %(dest,dest,' \\' if i<len(selected)-1 else ''))
(target/'lt02wifi-vendor-blobs.mk').write_text('\n'.join(lines)+'\n')
(target/'lt02wifi-vendor.mk').write_text('$(call inherit-product, vendor/samsung/lt02wifi-stockfull/lt02wifi-vendor-blobs.mk)\n')
report=Path('/home/airi/Tab3/stock-reference/full-vendor-inventory.txt')
report.write_text('Stock firmware: T210RUEU0COI1\nStock files selected: %d\nMissing existing vendor entries: %d\nAdded dependency files: %d\n\nMISSING (not included)\n%s\n\nADDED\n%s\n\nUNRESOLVED DT_NEEDED\n%s\n' %(len(selected),len(missing),len(added),'\n'.join(a+' -> '+b for a,b in missing),'\n'.join(added),'\n'.join(k+' needed by '+', '.join(v) for k,v in sorted(unresolved.items()))))
print('selected',len(selected),'omitted',len(missing),'added dependencies',len(added),'unresolved',len(unresolved))
print('\n'.join(k+' <- '+', '.join(v[:3]) for k,v in sorted(unresolved.items())))
