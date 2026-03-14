from z3 import *
import re
s = Solver()
flag = [BitVec(f'f_{i}',8) for i in range(40)]
regs =[BitVecVal(0,32) for _ in range(15) ]


input_file = 'main.cpp'

with open(input_file,'r') as f:
    content = f.read()

pattern =r'insn_t\s*\(\s*(\d+)\s*\,\s*(\d+)\s*\,\s*(\d+)\s*\)'
instructions = re.findall(pattern,content)


def solve_vm(instructions):
    global regs
    for opcode,op0,op1 in instructions:
        opcode,op0,op1 = int(opcode),int(op0),int(op1)

        if opcode == 0:
            regs[op0] = ZeroExt(24,flag[op1])
        elif opcode == 1:
            regs[op0] = BitVecVal(op1,32)
        elif opcode == 2:
            regs[op0] ^= BitVecVal(op1,32)
        elif opcode == 3:
            regs[op0] ^= regs[op1]
        elif opcode == 4:
            regs[op0] |= BitVecVal(op1,32)
        elif opcode == 5:
            regs[op0] |= regs[op1]
        elif opcode == 6:
            regs[op0] &= BitVecVal(op1,32)
        elif opcode == 7:
            regs[op0] &= regs[op1]
        elif opcode == 8:
            regs[op0] += BitVecVal(op1,32)
        elif opcode == 9:
            regs[op0] += regs[op1]
        elif opcode == 10:
            regs[op0] -= BitVecVal(op1, 32)
        elif opcode == 12:
            regs[op0] *= BitVecVal(op1, 32)
        elif opcode == 16:
            # 循环右移：Z3 提供了 RotateRight 函数 [cite: 17]
            regs[op0] = RotateRight(regs[op0], op1)
        elif opcode == 18:
            # 循环左移 [cite: 92, 105]
            regs[op0] = RotateLeft(regs[op0], op1)
        elif opcode == 20:
            regs[op0] = regs[op1]              # 赋值操作
        elif opcode == 21:
            regs[op0] = BitVecVal(0, 32)       # 清零
        elif opcode == 24:
            regs[op0] <<= op1
        elif opcode == 25:
            regs[op0] <<= regs[op1]


solve_vm(instructions)
s.add(regs[0] == 0x3ee88722)
s.add(regs[1]  == 0x0ecbdbe2)  # 注意：源码里是 0xecbdbe2，补齐是 0x0ecbdbe2
s.add(regs[2]  == 0x60b843c4)
s.add(regs[3]  == 0x05da67c7)
s.add(regs[4]  == 0x171ef1e9)
s.add(regs[5]  == 0x52d5b3f7)
s.add(regs[6]  == 0x3ae718c0)
s.add(regs[7]  == 0x8b4aacc2)
s.add(regs[8]  == 0xe5cf78dd)
s.add(regs[9]  == 0x4a848edf)
s.add(regs[10] == 0x8f)
s.add(regs[11] == 0x4180000)
s.add(regs[12] == 0x0)
s.add(regs[13] == 0xd)
s.add(regs[14] == 0x0)


s.add(flag[0] == ord('H'), flag[1] == ord('T'), flag[2] == ord('B'), flag[3] == ord('{'), flag[39] == ord('}'))
for f in flag:
    s.add(f>=32,f<=126)

if s.check() == sat:
    m = s.model()
    res = "".join([chr(m[f].as_long()) for f in flag])
    print(f"找到 Flag: {res}")
else:
    print("无解，请检查 opcode 映射或指令提取是否完整。")

