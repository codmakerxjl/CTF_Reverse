import re

input_file = 'main.cpp'
output_file= 'instructions.txt'

with open(input_file,'r') as f:
    content = f.read()

pattern =r'insn_t\s*\(\s*(\d+)\s*\,\s*(\d+)\s*\,\s*(\d+)\s*\)'
instructions = re.findall(pattern,content)

with open(output_file,'w') as f:
    for idx,(opcode,op0,op1) in enumerate(instructions):
        f.write(f'inst idx: {idx},opcode: {opcode},op0: {op0},op1: {op1}\n')


