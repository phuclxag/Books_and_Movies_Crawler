def pr(list):
    for i in list:
        yield i*i


a = pr([1,2,3])
for i in a:
    print(i)