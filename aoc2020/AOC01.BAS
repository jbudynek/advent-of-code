10 OPENIN "AOC-01.TXT"
20 a$="":DIM e%(200):n%=0
30 WHILE NOT EOF
40 LINE INPUT #9,a$
50 e%(n%)=VAL(a$): n%=n%+1
60 IF n% MOD 20=0 THEN PRINT "Reading expense ";n%;"=";a$
70 WEND
80 CLOSEIN
90 PRINT "Read ";n%;" expenses."
100 FOR i=0 TO 199
110 FOR j=i+1 TO 200
120 IF i MOD 5=0 AND j MOD 50=0 THEN PRINT "Looking up... i=";i;"j=";j;CHR$(11);
CHR$(13)
130 sum%=e%(i)+e%(j)
140 IF sum%=2020 GOTO 170
150 NEXT j:NEXT i
160 PRINT "Not found...":END
170 PRINT CHR$(10);"Found matching expenses!"
180 PRINT e%(i);"+";e%(j);"=2020"
190 PRINT "Answer=";e%(i)*e%(j):END
