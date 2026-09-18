"""Independent raw-polynomial check of a 40-point flat and S(f)=112.

This uses no logarithm tables and does not import the exhaustive diagnostic.
The resulting polynomial is safe and is not a distance counterexample.
"""
P = 0x1002D

def mul(a, b):
    ans = 0
    while b:
        if b & 1:
            ans ^= a
        b >>= 1
        a <<= 1
        if a & 65536:
            a ^= P
    return ans

def power(a, n):
    ans = 1
    while n:
        if n & 1:
            ans = mul(ans, a)
        a = mul(a, a)
        n >>= 1
    return ans

def rem(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a

def gcd(a, b):
    while b:
        a, b = b, rem(a, b)
    return a

assert power(2, 65536) == 2
assert gcd(P, power(2, 256) ^ 2) == 1  # Rabin, degree 16.
assert all(power(2, 65535 // p) != 1 for p in [3, 5, 17, 257])
E = [0, 1, power(2, 21845), power(2, 43690)]
U = {a ^ mul(b, 10) ^ mul(c, 15508) for a in E for b in E for c in E}
assert len(U) == 64
v, r = 306, 44234
assert v not in U
assert sum(power(v ^ u, 21845) == r for u in U) == 40
qcoeff = {1: 18286, 4: 25797, 16: 9130, 64: 1}

def evaluate(coeff, x):
    ans = 0
    for e, a in coeff.items():
        ans ^= mul(a, power(x, e))
    return ans

assert all(evaluate(qcoeff, u) == 0 for u in U)
scale = next(power(2, j) for j in range(3)
             if mul(power(power(2, j), 21845), r) == 1)
qv = evaluate(qcoeff, v)
assert qv
coeff = {e: mul(a, power(mul(power(scale, e), qv), 65534))
         for e, a in qcoeff.items()}
points = {mul(scale, u ^ mul(a, v)) for u in U for a in E}
assert len(points) == 256
assert all(evaluate(coeff, x) in E for x in points)
# f^4+f has degree 256, so these are all its F-rational roots.
S = 0
counts = {a: 0 for a in E}
for x in points:
    y = evaluate(coeff, x)
    counts[y] += 1
    phase = mul(y, power(x, 21845))
    trace = phase ^ mul(phase, phase)
    assert trace in [0, 1]
    S += 1 if trace == 0 else -1
assert all(count == 64 for count in counts.values())
assert S == 112
print("field polynomial:", hex(P), "F4:", E)
print("40-point witness: U=span_F4(1,10,15508), v=306, norm=44234")
print("input scale:", scale, "Q_U(v):", qv)
print("f coefficient dictionary:", coeff)
print("exact S:", S, "binary weight:", (1 << 29) - 8192 * S)
