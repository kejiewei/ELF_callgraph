#!/usr/bin/python
# powerpc-gekko-objdump -d example.elf | python cg.py | dot -Tpng > cg.png && eog cg.png

import re, sys
import os

f_re = re.compile('^[0-9a-f]* <([a-zA-Z0-9_]*)>:$')

jump_lst = '''b
bcl\-
beq\-
beq\+
bge\-
bge\+
bgt\-
bgt\+
bl
ble\-
blt\-
blt\+
bne\-
bne\+'''
c_re = re.compile("\t(%s) *[0-9a-f]* <([a-zA-Z0-9_]*)>" % '|'.join(jump_lst.split('\n')))

_blacklist = set(['sys_init', 'SYS_ResetSystem', 'puts', 'getButtons',
    'malloc', 'free', 'memalign', 'fflush', 'sd_mkdir', 'check_fatpath',
    'memset', 'memcpy', 'DCFlushRange', 'iosAlloc', 'iosFree',
    'DCInvalidateRange'])
_blacklist_pre = ['__', 'str', 'f_', 'VIDEO_']
_blacklist_cont = ['printf']
_blacklist_cont = ['printf']

def blacklist(s):
    for f in _blacklist_cont:
        if f in s: return True
    for f in _blacklist_pre:
        if s.startswith(f): return True
    if s in _blacklist: return True

def cppfilt(s):
    #cmd = "echo %s | powerpc-linux-gnu-c++filt | awk -F '(' '{print $1}'" % s
    cmd = "echo %s | powerpc-linux-gnu-c++filt" % s
    result = os.popen(cmd).read().strip()
    return result
    #return result.strip().split(':')[-1]
    #return s


cg = {}
for line in sys.stdin:
    line = line.strip()
    m = f_re.match(line)
    if m: s = cg[m.group(1)] = []

    m = c_re.search(line)
    if m and not blacklist(m.group(2)): s.append(m.group(2))
       
print "digraph g {"

l = ['main']
ls = set(l)
for i in l:
    #print "%s;" % i
    print "%s;" % cppfilt(i)
    for g in cg[i]:
        if g in ls: continue
        ls.add(g)
        l.append(g)

for i in ls:
    s = set()
    for j in cg[i]:
        if j not in s:
            s.add(j)
            #print "%s -> %s;" % (i, j);
	    print "%s -> %s" % (cppfilt(i), cppfilt(j))
print "}"
