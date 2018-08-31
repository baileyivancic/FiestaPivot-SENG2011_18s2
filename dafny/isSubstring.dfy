predicate hasSubstring(token: seq<char>,str: seq<char>)
{
	(exists i: nat :: i + |token| <= |str| && hasSubstringWithOffset(token,str,i))
}

predicate hasSubstringWithOffset(token: seq<char>, str: seq<char>, i: nat)
{ 
	// "<=" means "is token a prefix of str[i..]"
	(i + |token| <= |str|) && (token <= str[i..])
}

predicate loopInvariantOnEntry(token:string,str:string,i:int)
{
	exists n : int :: 0 <= n <= i && (n + |token| <= |str|) && hasSubstringWithOffset(token,str,n)  
}

method isSubstring(token: string, str: string) returns (r: bool)
	requires |str| > 0 && |token| > 0
	requires |token| <= |str|
	ensures r <==> hasSubstring(token,str)
  //ensures !r ==> (forall k : nat | k <= (|str| - |token|) :: !hasSubstringWithOffset(token,str,k))
{
	var i := 0;
	r := (token <= str[i..]);
	while(i <= (|str|-|token|) && !r)
		invariant r <== loopInvariantOnEntry(token,str,i)
		invariant r ==> (exists n : int :: (n >= 0) && (n + |token| <= |str|) && (token <= str[n..]))
    //invariant !r ==> (forall k : nat | k <= i <= |str|-|token| :: !hasSubstringWithOffset(token,str,k))
		invariant r ==> hasSubstringWithOffset(token,str,i)
		decreases |str|-|token|-i
	{
		if (token <= str[(i+1)..])
		{
			r := true;
		}
		i := i+1;
	}
}

method Main() {
	var token, str := "World","Hdwadaw World";
	assert token[..] == "World";
	assert str[..] == "Hdwadaw World";
  
	var found := isSubstring(token, str);

	assert (found == true) by
	{
		calc {
			token <= str[8..]; 
			hasSubstringWithOffset(token,str,8);
			hasSubstring(token,str);
			found == true;
		}
	}
}