import numpy as np;
import math;

# Helper Functions

def read_endf_line(line):
	#slice the first 66 characters
	line = line[0:65];
	#split the line into 11 width segments
	E = [];
	Edata = [];
	xs = [];
	xsdata = [];
	E.append(line[0:10]);
	xs.append(line[11:21]);
	E.append(line[22:32]);
	xs.append(line[33:43]);
	E.append(line[44:54]);
	xs.append(line[55:65]);
	for string in E:
		if not string.isspace():
			#determine positive or negative by the first character
			posneg = 1;
			if string[0] is '-':
				posneg = -1;
			#find the next + or -
			place = string.rfind('-');
			if place <= 0:
				place = string.rfind('+');
			#slice into pre and post
			pre = string[:place-1];
			post = string[place:];
			#calculate the float
			print E
			E = float(pre)
			E = E * 10.0**float(post)
			Edata.append(E);
	for string in xs:
		if not string.isspace():
			#determine positive or negative by the first character
			posneg = 1;
			if string[0] is '-':
				posneg = -1;
			#find the next + or -
			place = string.rfind('-');
			if place <= 0:
				place = string.rfind('+');
			#slice into pre and post
			pre = string[:place-1]
			post = string[place:]
			#calculate the float
			xs = float(pre)
			xs = xs * 10.0**float(post)
			xsdata.append(xs);
	return (np.array(Edata),np.array(xsdata));

def import_endf(filename):
	data = [line.strip() for line in open(filename, 'r')];
	#find the line ending with 099999
	(start_end,) = np.where([line.endswith("099999") for line in data]);
	#skip the next four lines
	if len(start_end) > 1:
		data = np.array(data[start_end[0]+5:start_end[1]])
		#read in the lines between this and the next 099999
	else:
		start_at_line_four = True

	E = [0.0];
	xs = [0.0];
	counter = 1
	for line in data:
		if (start_at_line_four and counter > 3 and not line.endswith("099999")) or (not start_at_line_four):
			(Edata,xsdata) = read_endf_line(line);
			for erg in Edata:
				E.append(erg);
			for sigma in xsdata:
				xs.append(sigma);
		counter = counter + 1
	E.append(np.max(E)+1.0);
	xs.append(0.0);
	E = np.array(E)/1.0E6; # convert to MeV
	return (E,np.array(xs));
