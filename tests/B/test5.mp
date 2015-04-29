{
output should be:
1
2
3
4
5
6
7
8
9
10
11
10
9
8
7
6
5
4
3
2
1
0
1
4
2
5
3
6
4
7
8
5
}

program testall;

var a: integer; b: integer; c: integer; d: integer; 

begin

    c := 0;

    repeat
        c := c + 1;
        writeln(c);
    until c > 10;

    WHILE c > 0 DO
    begin
       c := c - 1;
       writeln(c);
    end;

    c := 4;
    for d := 1 to c do
     begin
        Writeln(d);
        Writeln(c);
        c := c + 1;
     end;

    writeln(c);

        a := 3;
    b := 4;

        c := 20 div b;
        writeln(c);

    IF NOT (a < b) THEN
      WRITELN(a);


end.