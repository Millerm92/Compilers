program Test1;

{One Line Comment}

var
  answer, iterator, input, i: integer;  
  yes, no: boolean;
  randomstring:string;

{ 
  Multiple Line Comment
}

const 
  x = 10;
  y = 5;
  z = 'denbigh';  

begin
iterator := 0;
yes := true;
no := false;
randomstring := '1,3;:"fj309hga ; \\[\;;=-92.-%$@&(@*!          ';

  answer := x + y;
  write('answer: ');
  writeln(answer);            
  
  answer := x - y;
  write('answer: ');
  writeln(answer);            
  
  answer := x * y;
  write('answer: ');
  writeln(answer);            
  
  answer := x div y;
  write('answer: ');
  writeln(answer);     
       
  
  if(x > y) then begin
    repeat        
      write(iterator);
      write(' ');   
      writeln(z); 
      iterator := iterator + 1;
    until iterator >= 5;
  end;   
                 
  if(no) then begin
    writeln('0 this should not write');
  end else begin 
    if(yes) then begin  
      writeln('yes');
    end;
  end;  
           
  if(not(no) and (yes) and (x = 10)) then begin
    writeln('no yes 10');
  end;
  
  if((x < 2) or (not yes)) then begin
    writeln('1 this should not write');
  end;    
  
  if((x > 2) or (y < 100)) then begin
    writeln('x > 2 y < 100');
  end;          
  
  writeln(randomString);    
  
  read(input);
  write('you input: ');
  writeln(input);
              
  write('this should equal 50: ');
  writeln(x * y)  
  
  write('this should equal 31250: ');
  writeln(y * y * y * y * y * x);    
  
  writeln((((('lots of parentheses)))))')))));
  
  for i := 10 downto y do
    writeln(i);    
    
  for i := 0 to y do
    writeln(i); 
  
  while( i < 10) do 
  begin
    write(i);
    i := i + 1;
  end;         
  
  writeln('');
    
  while(i < 20) and (i > 0) do  
  begin
    write(i);
    write(' ');
    i := i +1; 
  end;
  
end.                               
  
