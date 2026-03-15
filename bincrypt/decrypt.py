from z3 import *

def solve_complete():
    s= Solver()

    input_chars = [BitVec(f'f_{i}',8) for i in range(28)]
    a1 = list(input_chars)

    def swap(arr,i,j):
        arr[i],arr[j] = arr[j],arr[i]

    swap(a1,0,12)
    swap(a1,14,26)
    swap(a1,4,8)
    swap(a1,20,23)

    v8=[9,12,2,10,4,1,6,3,8,5,7,11,0,13]
    v7=[2,4,6,8,11,13]

    def encodefunc(a1,a2):
        curr = a1
        for _ in range(8):
            src = [None]*14
            for i in range(14):
                src[i] = curr[v8[i]]
            curr = src
        for j in range(6):
            curr[v7[j]] ^= a2
        return curr
    
    part1 = a1[:14]
    part2 = a1[14:]

    encode_part1 = encodefunc(part1,2)
    encode_part2 = encodefunc(part2,3)

    encode_all = encode_part1+ encode_part2
    target = 'RV{r15]_vcP3o]L_tazmfSTaa3s0'

    for i in range(28):
        s.add(encode_all[i] == ord(target[i]))

    for  i in range(28):
        s.add(input_chars[i] >=32, input_chars[i] <= 126)

    if s.check() == sat:
        m = s.model()
        res = "".join([chr(m[input_chars[i]].as_long()) for i in range(28)])
        print(f"Flag: {res}")

solve_complete()

