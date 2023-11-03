# Group of Permutation

From the question on the description. The goal is to find order of Permutation Group to get the flag.

## Analysis


it is the same as RSA style to get the d where e*d = 1 mod order.

the order of permutation group with degree n is n factorial.

so if you have the order, then you get the d and then you get the G then you got the flag.
The step.

1. order = factorial(n)
2. d = inverse_mod(e, order) # because we know the length of P same as G, we know the value of e.
3. G = P ** d
4. reverse the permutation back.

