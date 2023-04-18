# TODO: make this into a Jupyter notebook

# large prime numbers
p = 199933
q = 16661
assert ((p-1)/q) % 1.0 == 0

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

import time
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

import hashlib
def hash_str(str):
    return hashlib.sha256(str.encode('utf-8')).hexdigest()
def hash(x):
    return int(hash_str(str), 16)

print(hash_str("this is a test of SHA-256"))
print(hash_str("hi"))
print(hash_str("Hi"))
print(hash_str("hi"))

# DSA signature scheme setup
h = 2
g = pow(h, (p-1)//q, p)
dsa_params = (p, q, g)

import random
def dsa_keygen():
   sk = random.randint(1, q-1) # secret key
   vk = pow(g, sk, p)
   return (sk, vk)

def dsa_sign(message, sk):
    k = random.randint(1, q-1)
    r = pow(g, k, p) % q
    k_inv = pow(k, -1, q)
    s = (k_inv * (hash(message) + sk * r)) % q
    if r == 0 or s == 0:
        return dsa_sign(message, sk)
    return (r, s)

print(dsa_sign("test", dsa_keygen()[0]))

def dsa_verify(message, signature, vk):
    r = signature[0]
    s = signature[1]
    w = pow(s, -1, q)
    u1 = (hash(message) * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(vk, u2, p)) % p) % q
    return v == r

keys = dsa_keygen()
print(dsa_verify("test", dsa_sign("test", keys[0]), keys[1]))
print(dsa_verify("test", dsa_sign("test", keys[1]), keys[1]))
long_message = "hfahkjhkjadshfkjhvaskjdhvfahskd" + hash_str("dhsfj") + hash_str("jksdjfk")
print(long_message)
print(dsa_verify(long_message, dsa_sign(long_message, keys[0]), keys[1]))
print(dsa_verify(long_message, dsa_sign(long_message, keys[1]), keys[1]))
