{Math test
  Output:
  14
  15
  7
  14
  2
  7
  5
  21
  
}
program mathTest;
var a, b, c, d, e, f: integer;
begin

b := 2;
c := 5;

a :=  b + c;
d := c - b;
e := b*a;
f := c*d;

write(e);
write(f);

write(a);
a := e mod f;
write( a );

write (b);
b := a div b;
write (b);

write(c);
c := f div c * b;
write(c);


end.