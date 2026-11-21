
 // Draws a rectangle at the top-left of the screen
 // The height is stored in RAM[0]

@0
D=M
@END
D;JLE

@SCREEN
D=A
@1
M=D

@0
D=M
@2
M=D

(LOOP)
@2
D=M
@END
D;JLE

@1
A=M
M=-1

@1
D=M
@32
D=D+A
@1
M=D

@2
M=M-1

@LOOP
0;JMP

(END)
@END
0;JMP
