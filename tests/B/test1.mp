{boolean test
    Output:
    0
    1
    0
    1
    0
    1
    1
    1 HERE
    0
    1
    10
    10
    1
    1
    1
    1

    
}
program ifTest;
var a, b: integer;
begin

a := 1;
b := 10;

writeln(a = b);
writeln(a < b);
writeln( a > b);
writeln(a <= b);
writeln(a >= b);
writeln(a <> b);





if (a < b) then
    writeln(a)
else
    writeln(b);

if (a > b) then
    writeln(a)
else
    writeln(b);

if (a <= b) then
    writeln(a)
else
    writeln(b);

if (a >= b) then
    writeln(a)
else
    writeln(b);

if (a = b) then
    writeln(a)
else
    writeln(b);

if (a <> b) then
    writeln(a) 
else
    writeln(b);


{Boolean operations with complex expressions}
if ( 1+8 > 8 ) then
    writeln(1)
else
    writeln(0);


if ( 20 mod 4 * 5 = 0 ) then
    writeln(1)
else
    writeln(0);


if ((20+4) div (3+3) > -10000 mod (63+14)) then
    writeln(1)
else
    writeln(0);



end.