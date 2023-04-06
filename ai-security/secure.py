import hashlib
import time

def hash(str):
    return hashlib.sha256(str.encode('utf-8')).hexdigest()

p = 199933
q = 16661
assert ((p-1)/q)%1.0 == 0

def fast_exp(base, exp):
    # O(log n)
    res = pow(base, exp//2, p)
    res = pow(res, 2, p)
    if exp % 2 == 1:
        res *= base
        res %= p
    return res
def slow_log(base, num):
    # O(n)
    res = 0
    while num > 1:
        num *= pow(base, -1, p)
        num %= p
        res += 1
    return res

def time_exp_log(base, exp):
    print("Timing %d^%d" % (base,exp))
    start_exp = time.time()
    do_pow = fast_exp(base, exp)
    exp_time = (time.time()-start_exp)*1000000
    start_log = time.time()
    do_log = slow_log(base, do_pow)
    log_time = (time.time()-start_exp)*1000000
    assert do_log == exp

    print("Exponentiation time: %f µs" % (exp_time))
    print("Logarithm time: %f µs" % (log_time))
    print("Ratio: %f\n" % (log_time/exp_time))
time_exp_log(3, 500)
time_exp_log(4, 500)
time_exp_log(2, 1000)

print(hash("hi"))
print(hash("Hi"))
print(hash("hi"))
