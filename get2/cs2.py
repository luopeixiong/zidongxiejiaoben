a = dict({'0': 1})
k = '_0_'
a[k] = {}
a[k]['0'] = 1
print(a)

# {'a': {'0': 0}} {'a': {'0': 0, '1': 0}}