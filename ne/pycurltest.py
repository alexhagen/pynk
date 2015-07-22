import pycurl
from StringIO import StringIO

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
			Edata.append(float(pre)*10.0**float(post));
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
			pre = string[:place-1];
			post = string[place:];
			#calculate the float
			xsdata.append(float(pre)*10.0**float(post));
	return (np.array(Edata),np.array(xsdata));

def import_endf(filename):
	data = [line.strip() for line in open(filename, 'r')];
	#find the line ending with 099999
	(start_end,) = np.where([line.endswith("099999") for line in data]);
	#skip the next four lines
	data = np.array(data[start_end[0]+5:start_end[1]])
	#read in the lines between this and the next 099999

	E = [0.0];
	xs = [0.0];
	for line in data:
		(Edata,xsdata) = read_endf_line(line);
		for erg in Edata:
			E.append(erg);
		for sigma in xsdata:
			xs.append(sigma);
	E.append(np.max(E)+1.0);
	xs.append(0.0);
	E = np.array(E)/1.0E6; # convert to MeV
	return (E,np.array(xs));

# read in the table from endf
s = '''
<TABLE CELLPADDING="5">
<TR>
<TD><I><B>1-H</B></I></TD>
  <TD><I><B>-2</B></I></TD>
    <TD>128</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/H/2">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/H/2">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/h/2.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>4-Be</B></I></TD>
  <TD><I><B>-9</B></I></TD>
    <TD>425</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Be/9">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Be/9">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/be/9.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>6-C</B></I></TD>
  <TD><I><B>-12</B></I></TD>
    <TD>625</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/C/12">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/C/12">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/c/12.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><BR></TD>
  <TD><I><B>-13</B></I></TD>
    <TD>628</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/C/13">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/C/13">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/c/13.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>7-N</B></I></TD>
  <TD><I><B>-14</B></I></TD>
    <TD>725</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/N/14">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/N/14">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/n/14.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><BR></TD>
  <TD><I><B>-15</B></I></TD>
    <TD>728</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/N/15">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/N/15">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/n/15.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>8-O</B></I></TD>
  <TD><I><B>-16</B></I></TD>
    <TD>825</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/O/16">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/O/16">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/o/16.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><BR></TD>
  <TD><I><B>-17</B></I></TD>
    <TD>828</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/O/17">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/O/17">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/o/17.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><BR></TD>
  <TD><I><B>-18</B></I></TD>
    <TD>831</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/O/18">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/O/18">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/o/18.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>11-Na</B></I></TD>
  <TD><I><B>-23</B></I></TD>
    <TD>1125</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Na/23">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Na/23">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/na/23.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>12-Mg</B></I></TD>
  <TD><I><B>-24</B></I></TD>
    <TD>1225</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mg/24">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mg/24">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mg/24.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-25</B></I></TD>
    <TD>1228</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mg/25">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mg/25">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mg/25.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-26</B></I></TD>
    <TD>1231</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mg/26">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mg/26">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mg/26.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>13-Al</B></I></TD>
  <TD><I><B>-27</B></I></TD>
    <TD>1325</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Al/27">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Al/27">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/al/27.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>14-Si</B></I></TD>
  <TD><I><B>-28</B></I></TD>
    <TD>1425</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Si/28">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Si/28">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/si/28.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-29</B></I></TD>
    <TD>1428</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Si/29">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Si/29">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/si/29.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-30</B></I></TD>
    <TD>1431</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Si/30">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Si/30">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/si/30.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>16-S</B></I></TD>
  <TD><I><B>-32</B></I></TD>
    <TD>1625</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/S/32">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/S/32">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/s/32.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-33</B></I></TD>
    <TD>1628</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/S/33">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/S/33">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/s/33.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-34</B></I></TD>
    <TD>1631</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/S/34">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/S/34">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/s/34.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-36</B></I></TD>
    <TD>1637</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/S/36">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/S/36">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/s/36.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>17-Cl</B></I></TD>
  <TD><I><B>-35</B></I></TD>
    <TD>1725</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cl/35">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cl/35">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cl/35.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-37</B></I></TD>
    <TD>1731</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cl/37">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cl/37">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cl/37.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>18-Ar</B></I></TD>
  <TD><I><B>-36</B></I></TD>
    <TD>1825</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ar/36">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ar/36">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ar/36.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-38</B></I></TD>
    <TD>1831</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ar/38">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ar/38">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ar/38.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-40</B></I></TD>
    <TD>1837</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ar/40">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ar/40">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ar/40.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>20-Ca</B></I></TD>
  <TD><I><B>-40</B></I></TD>
    <TD>2025</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ca/40">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ca/40">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ca/40.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-42</B></I></TD>
    <TD>2031</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ca/42">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ca/42">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ca/42.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-43</B></I></TD>
    <TD>2034</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ca/43">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ca/43">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ca/43.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-44</B></I></TD>
    <TD>2037</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ca/44">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ca/44">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ca/44.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-46</B></I></TD>
    <TD>2043</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ca/46">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ca/46">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ca/46.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-48</B></I></TD>
    <TD>2049</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ca/48">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ca/48">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ca/48.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>22-Ti</B></I></TD>
  <TD><I><B>-46</B></I></TD>
    <TD>2225</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ti/46">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ti/46">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ti/46.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-47</B></I></TD>
    <TD>2228</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ti/47">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ti/47">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ti/47.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-48</B></I></TD>
    <TD>2231</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ti/48">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ti/48">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ti/48.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-49</B></I></TD>
    <TD>2234</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ti/49">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ti/49">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ti/49.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-50</B></I></TD>
    <TD>2234</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ti/50">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ti/50">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ti/50.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>23-V</B></I></TD>
  <TD><I><B>-51</B></I></TD>
    <TD>2328</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/V/51">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/V/51">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/v/51.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>24-Cr</B></I></TD>
  <TD><I><B>-50</B></I></TD>
    <TD>2425</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cr/50">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cr/50">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cr/50.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-52</B></I></TD>
    <TD>2431</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cr/52">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cr/52">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cr/52.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-53</B></I></TD>
    <TD>2434</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cr/53">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cr/53">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cr/53.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-54</B></I></TD>
    <TD>2437</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cr/54">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cr/54">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cr/54.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>25-Mn</B></I></TD>
  <TD><I><B>-55</B></I></TD>
    <TD>2525</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mn/55">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mn/55">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mn/55.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>26-Fe</B></I></TD>
  <TD><I><B>-54</B></I></TD>
    <TD>2625</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Fe/54">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Fe/54">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/fe/54.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-56</B></I></TD>
    <TD>2631</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Fe/56">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Fe/56">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/fe/56.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-57</B></I></TD>
    <TD>2634</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Fe/57">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Fe/57">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/fe/57.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-58</B></I></TD>
    <TD>2637</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Fe/58">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Fe/58">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/fe/58.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>27-Co</B></I></TD>
  <TD><I><B>-59</B></I></TD>
    <TD>2725</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Co/59">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Co/59">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/co/59.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>28-Ni</B></I></TD>
  <TD><I><B>-58</B></I></TD>
    <TD>2825</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ni/58">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ni/58">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ni/58.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-60</B></I></TD>
    <TD>2831</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ni/60">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ni/60">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ni/60.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-61</B></I></TD>
    <TD>2834</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ni/61">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ni/61">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ni/61.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-62</B></I></TD>
    <TD>2837</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ni/62">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ni/62">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ni/62.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-64</B></I></TD>
    <TD>2843</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ni/64">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ni/64">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ni/64.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>29-Cu</B></I></TD>
  <TD><I><B>-63</B></I></TD>
    <TD>2925</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cu/63">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cu/63">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cu/63.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-65</B></I></TD>
    <TD>2931</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cu/65">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cu/65">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cu/65.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>30-Zn</B></I></TD>
  <TD><I><B>-64</B></I></TD>
    <TD>3025</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zn/64">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zn/64">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zn/64.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-66</B></I></TD>
    <TD>3031</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zn/66">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zn/66">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zn/66.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-67</B></I></TD>
    <TD>3034</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zn/67">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zn/67">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zn/67.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-68</B></I></TD>
    <TD>3037</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zn/68">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zn/68">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zn/68.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-70</B></I></TD>
    <TD>3043</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zn/70">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zn/70">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zn/70.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>32-Ge</B></I></TD>
  <TD><I><B>-70</B></I></TD>
    <TD>3225</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ge/70">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ge/70">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ge/70.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-72</B></I></TD>
    <TD>3231</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ge/72">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ge/72">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ge/72.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-73</B></I></TD>
    <TD>3234</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ge/73">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ge/73">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ge/73.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-74</B></I></TD>
    <TD>3237</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ge/74">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ge/74">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ge/74.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-76</B></I></TD>
    <TD>3243</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ge/76">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ge/76">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ge/76.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>38-Sr</B></I></TD>
  <TD><I><B>-84</B></I></TD>
    <TD>3825</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sr/84">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sr/84">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sr/84.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-86</B></I></TD>
    <TD>3831</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sr/86">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sr/86">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sr/86.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-87</B></I></TD>
    <TD>3834</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sr/87">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sr/87">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sr/87.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-88</B></I></TD>
    <TD>3837</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sr/88">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sr/88">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sr/88.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-90</B></I></TD>
    <TD>3843</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sr/90">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sr/90">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sr/90.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>40-Zr</B></I></TD>
  <TD><I><B>-90</B></I></TD>
    <TD>4025</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zr/90">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zr/90">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zr/90.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-91</B></I></TD>
    <TD>4028</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zr/91">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zr/91">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zr/91.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-92</B></I></TD>
    <TD>4031</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zr/92">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zr/92">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zr/92.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-93</B></I></TD>
    <TD>4034</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zr/93">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zr/93">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zr/93.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-94</B></I></TD>
    <TD>4037</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zr/94">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zr/94">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zr/94.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-96</B></I></TD>
    <TD>4043</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Zr/96">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Zr/96">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/zr/96.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>41-Nb</B></I></TD>
  <TD><I><B>-93</B></I></TD>
    <TD>4125</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Nb/93">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Nb/93">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/nb/93.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-94</B></I></TD>
    <TD>4128</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Nb/94">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Nb/94">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/nb/94.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>42-Mo</B></I></TD>
  <TD><I><B>-92</B></I></TD>
    <TD>4225</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mo/92">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mo/92">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mo/92.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-94</B></I></TD>
    <TD>4231</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mo/94">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mo/94">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mo/94.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-95</B></I></TD>
    <TD>4234</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mo/95">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mo/95">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mo/95.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-96</B></I></TD>
    <TD>4237</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mo/96">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mo/96">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mo/96.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-97</B></I></TD>
    <TD>4240</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mo/97">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mo/97">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mo/97.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-98</B></I></TD>
    <TD>4243</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mo/98">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mo/98">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mo/98.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-100</B></I></TD>
    <TD>4249</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Mo/100">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Mo/100">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/mo/100.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>47-Ag</B></I></TD>
  <TD><I><B>-107</B></I></TD>
    <TD>4725</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ag/107">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ag/107">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ag/107.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-109</B></I></TD>
    <TD>4731</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ag/109">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ag/109">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ag/109.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>53-I</B></I></TD>
  <TD><I><B>-127</B></I></TD>
    <TD>5325</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/I/127">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/I/127">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/i/127.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-129</B></I></TD>
    <TD>5331</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/I/129">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/I/129">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/i/129.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>55-Cs</B></I></TD>
  <TD><I><B>-133</B></I></TD>
    <TD>5525</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cs/133">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cs/133">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cs/133.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-135</B></I></TD>
    <TD>5531</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cs/135">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cs/135">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cs/135.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-137</B></I></TD>
    <TD>5537</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Cs/137">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Cs/137">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/cs/137.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>59-Pr</B></I></TD>
  <TD><I><B>-141</B></I></TD>
    <TD>5925</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pr/141">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pr/141">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pr/141.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>62-Sm</B></I></TD>
  <TD><I><B>-144</B></I></TD>
    <TD>6225</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/144">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/144">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/144.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-147</B></I></TD>
    <TD>6234</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/147">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/147">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/147.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-148</B></I></TD>
    <TD>6237</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/148">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/148">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/148.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-149</B></I></TD>
    <TD>6240</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/149">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/149">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/149.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-150</B></I></TD>
    <TD>6243</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/150">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/150">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/150.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-151</B></I></TD>
    <TD>6246</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/151">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/151">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/151.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-152</B></I></TD>
    <TD>6249</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/152">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/152">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/152.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-154</B></I></TD>
    <TD>6255</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Sm/154">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Sm/154">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/sm/154.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>65-Tb</B></I></TD>
  <TD><I><B>-158</B></I></TD>
    <TD>6522</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Tb/158">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Tb/158">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/tb/158.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-159</B></I></TD>
    <TD>6525</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Tb/159">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Tb/159">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/tb/159.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>67-Ho</B></I></TD>
  <TD><I><B>-165</B></I></TD>
    <TD>6725</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ho/165">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ho/165">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ho/165.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>73-Ta</B></I></TD>
  <TD><I><B>-181</B></I></TD>
    <TD>7328</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Ta/181">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Ta/181">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/ta/181.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>74-W</B></I></TD>
  <TD><I><B>-180</B></I></TD>
    <TD>7425</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/W/180">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/W/180">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/w/180.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-182</B></I></TD>
    <TD>7431</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/W/182">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/W/182">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/w/182.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-183</B></I></TD>
    <TD>7434</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/W/183">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/W/183">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/w/183.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-184</B></I></TD>
    <TD>7437</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/W/184">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/W/184">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/w/184.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-186</B></I></TD>
    <TD>7443</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/W/186">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/W/186">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/w/186.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>79-Au</B></I></TD>
  <TD><I><B>-197</B></I></TD>
    <TD>7925</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Au/197">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Au/197">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/au/197.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>82-Pb</B></I></TD>
  <TD><I><B>-206</B></I></TD>
    <TD>8231</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pb/206">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pb/206">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pb/206.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-207</B></I></TD>
    <TD>8234</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pb/207">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pb/207">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pb/207.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-208</B></I></TD>
    <TD>8237</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pb/208">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pb/208">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pb/208.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>83-Bi</B></I></TD>
  <TD><I><B>-209</B></I></TD>
    <TD>8325</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Bi/209">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pb/209">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/bi/209.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>92-U</B></I></TD>
  <TD><I><B>-233</B></I></TD>
    <TD>9222</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/U/233">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/U/233">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/u/233.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-234</B></I></TD>
    <TD>9225</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/U/234">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/U/234">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/u/234.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-235</B></I></TD>
    <TD>9228</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/U/235">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/U/235">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/u/235.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-236</B></I></TD>
    <TD>9231</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/U/236">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/U/236">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/u/236.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-238</B></I></TD>
    <TD>9237</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/U/238">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/U/238">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/u/238.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>93-Np</B></I></TD>
  <TD><I><B>-237</B></I></TD>
    <TD>9346</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Np/237">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Np/237">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/np/237.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>94-Pu</B></I></TD>
  <TD><I><B>-238</B></I></TD>
    <TD>9434</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pu/238">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pu/238">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pu/238.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-239</B></I></TD>
    <TD>9437</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pu/239">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pu/239">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pu/239.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-240</B></I></TD>
    <TD>9440</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pu/240">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pu/240">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pu/240.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><BR></TD>
  <TD><I><B>-241</B></I></TD>
    <TD>9443</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Pu/241">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Pu/241">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/pu/241.pdf">view PDF plots</A></TD>
</TR>
<TR>
<TD><I><B>95-Am</B></I></TD>
  <TD><I><B>-241</B></I></TD>
    <TD>9543</TD>
    <TD><A HREF="../../data/data/ENDFB-VII-gamma/Am/241">raw eval</A></TD>
    <TD>
    <FORM METHOD="POST" ACTION="../../data/ndbrowse.php">
    <INPUT TYPE=hidden NAME="path" VALUE="../data/data/ENDFB-VII-gamma/Am/241">
    <INPUT TYPE=hidden NAME="mf" VALUE=0>
    <INPUT TYPE=hidden NAME="mt" VALUE=0>
    <INPUT TYPE="submit" VALUE="browse eval">
    </FORM>
    </TD>
    <TD><A HREF="endfvii-g-pdf/am/241.pdf">view PDF plots</A></TD>
</TR>
</TABLE>
'''
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(s, 'html.parser')
for row in soup.table.tr:
	print row.children;
'''

def letters(input):
    valids = []
    for character in input:
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)

def numbers(input):
    valids = []
    for character in input:
        if character.isdigit():
            valids.append(character)
    return int(''.join(valids));

from bs4 import BeautifulSoup
from urllib2 import urlopen
soup = BeautifulSoup(s,'lxml')
table = soup.find('table')
headers = [header.text for header in table.find_all('th')]
rows = []
for row in table.find_all('tr'):
    rows.append([val.text.encode('utf8') for val in row.find_all('td')]);

element = '';
for row in rows:
	if row[0] is not '':
		element = letters(row[0]);
	if row[1] is not '':
		isotope = numbers(row[1]);
	print "%s-%d" % (element,isotope);
	link = "https://t2.lanl.gov/nis/data/data/ENDFB-VII-gamma/%s/%d" % \
		(element,isotope);
# read in the data from endf

buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, link)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()
if "<title>404 Not Found</title>" in body:
	raise Exception('ENDF has no entry for that reaction on that nuclide');
else:
	print(body)
