
import re
a = "-"

print(re.sub(r'[^0-9]', '', a.split("(")[-1]))
