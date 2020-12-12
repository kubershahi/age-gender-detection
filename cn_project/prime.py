
# from Crypto.Util import number 

# p = number.getPrime(50) 
# print(p)
# q = number.getPrime(50)
# while p == q:
#     q = number.getPrime(50)
# print(q)

import random 

# function to generate n-bit prime number 
def get_prime(n):

    def nBitRandom(n): 
        return random.randrange(2**(n-1)+1, 2**n - 1) 

    # This function is called for all k trials. It returns false if n is composite and 
    # returns false if n is probably prime. d is an odd number such that d*2<sup>r</sup> = n-1 
    # for some r >= 1 

    def miller_test(n, d): 
        # Pick a random number in [2..n-2] 
        # Corner cases make sure that n > 4 
        a = 2 + random.randint(1, n - 4) 

        # Compute a^d % n 
        x = pow(a, d, n) 

        if (x == 1 or x == n - 1): 
            return True 

        # Keep squaring x while one 
        # of the following doesn't 
        # happen 
        # (i) d does not reach n-1 
        # (ii) (x^2) % n is not 1 
        # (iii) (x^2) % n is not n-1 
        while (d != n - 1): 
            x = (x * x) % n 
            d *= 2 

            if (x == 1): 
                return False 
            if (x == n - 1): 
                return True 

        # Return composite 
        return False 

    # It returns false if n is 
    # composite and returns true if n 
    # is probably prime. k is an 
    # input parameter that determines 
    # accuracy level. Higher value of 
    # k indicates more accuracy. 

    def isPrime(n, k): 
        if (n <= 1 or n == 4): # Corner cases 
            return False 
        if (n <= 3): 
            return True 

        # Find r such that n = 
        # 2^d * r + 1 for some r >= 1 
        d = n - 1 
        while (d % 2 == 0): 
            d //= 2 

        # Iterate given nber of 'k' times 
        j = 0
        while j < k:
            if (miller_test(n, d) == False): 
                return False
            j = j + 1
        return True

    x = nBitRandom(n) 
    # print(x)

    while not isPrime(x, 15):
        x = nBitRandom(n) 
        # print(x)
    return x

p = get_prime(50) 
print(p)
q = get_prime(50)
while p == q:
    q = get_prime(50)
print(q)


