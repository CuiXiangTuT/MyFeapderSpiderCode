from copy import deepcopy

d = {"a":1,"vv":22}

k = deepcopy(d)
print(k["vv"])