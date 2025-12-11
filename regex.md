# GREP
```bash
^			beginning of line
$			end of line
^$			blank line
''			single quotes to parse regex
grep -c			count
esc+.			last file typed
(x|x)			group and or operator - requires -E
grep -v			invert selection
grep -vE '^(#|$)'	remove commented lines & empty lines
BRE			Basic Regular Expressions
ERE			Enhanced regular expressions -E
grep -l			list file names that contain string ex. /etc/pam/* to select multiple files
!!			run complete last command
IFS			Internal Field Separator - default is white space
            echo "fred 23 sales" >> emp.txt .. while read name age dept do; \n echo $name \n echo $age \n echo $dept
            IFS='x' .. bash variable
process file		ex. IFS=':' .. while read n p u g p c d s ; do \n echo-e "User: $n\n\tPass: $p\n\tUID: .. etc
tr			translate ex. $ tr ' ' ',' < emp.txt ... translates space to ,  
```

# SED
```bash
sed -n '1p'		-n = supress standard output and only match pattern '1p' = print line 1 '$p' = print last line '1,3p' = lines 1 thru  3
sed '$a something'	print last line and append somthing
sed -i '$d' /file	-i = edit file in line '$d' = delete last line
sed -i '1i text' /file	'1i text' = insert before line 1
vim +$ /file		put cursor at end of file
vim +/ServerName/ file	takes to the line which contains the string
sed -n '/<string1/,/<\/string2/p' file  - prints block of text; string1 opening, string2 end of block
sed '/^$/d;/^#/d' 	; alternate syntax for or
file.sed		contains expressions; ex. sed -f file.sed file
sed -f test.sed -i.ba	create backup before editing
ssh flags		-C execute commands -n redirect stdin to /dev/null allowing remote execution on multiple servers
-i.bak			create backup of file when in place edit
t			test - if previous line in .sed file suceeded ex. ssh_client_alive.sed
p			print the patter space
//			delimited regex
a			append
i			insert before matched line
i.bak			will create a backup file
d			deletes the line that matches
```

# AWK
## main block
awk 			begin block = print headers; main block=print fields; end block = summary
-F[separator]			field separator
NR			print number of row
$0			complete line
$[number]		number of field delimited by field separator
print			output to stdout
printf			for better format / alignment - makes ref to C module - specify formatting first ex. awk -F: '{ printf "%2%S%s6d\n",NR, ": ", $1, $3}' /etc/passwd
%			begins any format specifier; %2d = digit decimal number; %s = string
%s			string; ex. %20s = width of string
\n			newline
```

```bash
*begin block**		used for setting headers as well as set variables
BEGIN			starts begin block; 
;			new statement
++			increment
FS			Field Separator
OFS			Output Field Separator
```

```bash
## end block		used for summary
END			starts the end block
```

```bash
awk files		see passwd.awk
ex. 			awk 'BEGIN {FS=":"; printf "%4s%20s%6s\n", "Num:", "username", "UID"; COUNT=0} /bash$/{ COUNT++; printf "%2d%s%20s%6d\n",COUNT, ": ", $1, $a3} END { print "We have " NR " users, of which " COUNT " use BASH" }' /etc/passwd
```

# STRINGS AND REGEX CHARACTERS
## Anchors
```bash
^			beginning of line
$			end of line
```
## Ranges
```bash
(x|x)			or
[]			ranges
[^]			^ inside range negates following character
```
## Boundaries
```bash
\s			any whitespace
\b			word boundry, space; hyphen
\S or \B 		Capitol reverses the meaning
```
## Quantifiers
```bash
?			0 or 1 of the previous character
*			zero or more of the previous character
+			one or more of the previous character
{3}			matched exactly the number inside braces of the previous character
{1,2}			1 or 2 of the previous character
.			single character
```
