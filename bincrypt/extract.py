
input_file = 'file.bin'
output_file = 'hidden.bin'


with open(input_file,'rb') as f_in , open(output_file,'wb') as f_out:
    content = f_in.read()
    
    translate_data = bytes([ b^0xAB for b in content ])
    f_out.write(translate_data)




