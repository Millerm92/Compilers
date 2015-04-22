program mathTest;
var a, b, c, d, e, f: boolean;
x, y, z : integer;

begin

x := 1;
y := 2;
z := 3;

writeln(a);

b := true;
writeln(b);

c := not b;
writeln(c);

d :=  b and c;
writeln(d);

e  := x < y;
writeln(e);

e := (x < y) and (y < z);
writeln(e);

f:= b*a;
writeln(f);

f := c*d;
writeln(f);

end.