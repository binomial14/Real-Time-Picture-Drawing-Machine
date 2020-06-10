import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

i_f = open(input_file,'r')
o_f =open(output_file,'w')

up_or_not = False
write_down = False
pass_paragraph = False
for line in i_f:
	if line[0:22] == "(Start cutting path id":
		pass_paragraph = not pass_paragraph
	elif pass_paragraph and line[0:22] == "(Start cutting path id":
		pass_paragraph = not pass_paragraph
		o_f.write(line)
		o_f.flush()
	elif not pass_paragraph:
		if line == "G00 Z5.000000\n":
			up_or_not = not up_or_not
			if up_or_not:
				o_f.write("M3 S25\n")
				o_f.flush()
				write_down = True
		else:
			if line[0:7] == "G01 Z-0" or line[0:2] == "M5":
				continue
			if line[0:8] == "(Footer)":
				o_f.write("M3 S25\n")
			o_f.write(line)
			if write_down:
				o_f.write("M3 S0\n")
				o_f.flush()
				write_down = False

	

#print(c)


