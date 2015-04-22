{
    Input :
        a = 5
        b = 10
        c = 20
        d = 4
        e = 100
    Output :
        100
        5
        100
        50
        5
        5
        15
        10
        88
        -66
        15
        -15
}

program writeTest;
var a, b, c, d, e : integer;

begin


{READ STATEMENT}
        {single read}
        read(a);

        {multi read}
        read(b,c,d,e);  
{END READ STATEMENT}



{WRITE STATEMENT}

        {write Factor -> unsigned int}
        writeln( 100 );

        {write Factor -> variable identifier}
        writeln (a);

        {write Factor ->"(" Expression ")" }
        writeln( (100) );

        {write Term -> Factor FactorTail}
                {write Term -> Factor      see the above operations}
                {write Term -> Factor MutiplyingOperator Factor FactorTail}
                        {write Term -> Factor "*" Factor FactorTail}
                        writeln( a * b );

                        {write Term -> Factor "div" Factor FactorTail}
                        writeln( c div d );

                        {write Term -> Factor "mod" Factor FactorTail}
                        writeln( a mod e );

    {write Simple Expression -> Term TermTail}
            {write SimpleExpression -> Term AddingOperator Term TermTail}
            {write SimpleExpression -> Term "+" Term TermTail}
            writeln(a + b);

            {write SimpleExpression -> Term "-" Term TermTail}
            writeln(c-b); 
    
    {write SimpleExpression -> OptionalSign Term TermTail}
        {write SimpleExpression -> "+" Term}
        writeln( + 88);
        
        {write SimpleExpression -> "-" Term}
        writeln(-66);
        
        {write SimpleExpression -> "+"  Term "+" Term TermTail} 
                writeln(+ a + b);

        {write SimpleExpression -> "-"  Term "+" Term TermTail}
                writeln(-(a + b));

    {write Expression -> Simple Expression OptionalRelationalPart}
        {write Epression -> SimpleExpression RelationalOperator SimpleExpression}
        {write Epression -> SimpleExpression "=" SimpleExpression}
        {write Epression -> SimpleExpression "<" SimpleExpression}
        {write Epression -> SimpleExpression ">" SimpleExpression}
        {write Epression -> SimpleExpression "<=" SimpleExpression}
        {write Epression -> SimpleExpression ">=" SimpleExpression}
        {write Epression -> SimpleExpression "<>" SimpleExpression}
        

{END WRITE STATEMENT}
end.