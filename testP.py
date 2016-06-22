# a=True
# if not a:
#     print 't'
def random_ascii(**kwargs):
    if kwargs.get("seed"):
       print '?'
    else:
        print '!'


if __name__ == '__main__':
    random_ascii(seed=1)