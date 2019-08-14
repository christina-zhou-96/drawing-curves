import re
import os

# list out all folders
dir = r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2018-19 SAT School Day Initiative\01 - Data'
os.walk(dir)

to_remove = [dir]
strings = [x[0] for x in os.walk(dir)]
p = re.compile('|'.join(map(re.escape, to_remove)))
new_list = [p.sub('', s) for s in strings]
print(*new_list, sep="\n")