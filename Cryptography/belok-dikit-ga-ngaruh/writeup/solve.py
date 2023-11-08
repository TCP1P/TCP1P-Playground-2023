from libnum import *
from Crypto.Util.number import *

lines = open("src/out.txt", "r").readlines()
nums = []
for line in lines:
    line = line.strip()
    if len(line) > 0:
        nums.append(int(line))

ct = nums[-1]
nums = nums[0:-1]
# recover n
# a0, a1, a2, a3, a4, ...
# ci = ai + ai+1
# di = ai+1 - ai = a (ai^2 - ai-1^2) = a * di-1 * ci-1
# di-1 = a * di-2 * ci-2
# di * di-2 * ci-2 - di-1 * di-1 * ci-1 = 0 (mod n)
d = []
c = []
for i in range(1, len(nums)):
    d.append(nums[i] - nums[i-1])
    c.append(nums[i] + nums[i-1])

n = 0
for i in range(0, len(d) - 2):
    cur = d[i+2] * d[i] * c[i] - d[i+1] * d[i+1] * c[i+1]
    n = GCD(cur, n)

assert(n != 0)

# recover a, b
# a0, a1, a2, a3, a4, ...
# a0^2 * a + b = a1 (mod n)
# (a0^2 - a1^2) * a = a1 - a2 (mod n)

rhs = (nums[1] - nums[2]) % n
lhs = (nums[0]**2 - nums[1]**2) % n
a = rhs * pow(lhs, -1, n)
a = a % n
b = (nums[1] - nums[0] * nums[0] * a) % n
key = (nums[-1] ** 2) * a + b
key %= n
print(n2s(key ^ ct))