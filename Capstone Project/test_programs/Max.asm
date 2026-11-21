// Computes the maximum of RAM[0] and RAM[1]
// Stores the result in RAM[2]

@0
D=M
@1
D=D-M
@NEGATIVE
D;JLT

@0
D=M
@2
M=D
@END
0;JMP

(NEGATIVE)
@1
D=M
@2
M=D

(END)
@END
0;JMP