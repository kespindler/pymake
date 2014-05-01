import re

# Types of paths
# 1. static strings
# 2. replacement strings
# 3. Matching strings

rule(re.compile("*\.o"), depends="{name}.c")

file('hello', action='{CC} {CFLAGS} {depends}' depends='hello.c')


