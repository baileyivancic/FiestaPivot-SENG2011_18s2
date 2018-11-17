predicate hasPrefix(token: string, str: string)
{
   (|token| == 0) || ((|token| <= |str|) && (token == str[..|token|]))
}

predicate hasNoPrefix(token:string, str:string)
{
	(|token| > |str|) || (token != str[..|token|])
}

predicate hasSubstring(token:string, str:string)
{
	(exists n : int :: (0 <= n < |str| + 1) && hasPrefix(token, str[n..]))
}

predicate hasNoSubstring(token:string, str:string)
{
	(forall n : int | (0 <= n < |str| + 1) :: hasNoPrefix(token,str[n..]))
}

method isPrefix(token: string, str: string) returns (r:bool)
   requires |token| >= 0 && |str| >= 0
	ensures (r == true) <==> hasPrefix(token,str)
	ensures (r == false) <==> hasNoPrefix(token,str)
{
	if (|token| == 0)
	{
		r:=true;
	}
	
   if (|str| < |token|)
	{
		r:=false;
	}
   else 
   {
      r:=(str[..|token|] == token);
   }
}

method isSubstring(token: string, str: string) returns (r:bool)
   requires |token| >= 0
   requires |str| >= 0
   requires |token| <= |str|
	ensures (r == true) ==> (|token| == 0) || hasSubstring(token, str)
	ensures (r == false) <==> hasNoSubstring(token, str)
{
   var m;
	var i := 0;
	r := false;
	while ((i < (|str| + 1)) && (r == false))
		invariant 0 <= i <= |str|+1
		invariant (r == true) ==> hasSubstring(token, str)
		invariant (r == false) <==> (forall l :: 0 <= l < i ==> hasNoPrefix(token, str[l..]))
		decreases |str| - i
	{
		m := isPrefix(token, str[i..]);
		if (m == true) {
			r := true;
		}
		i := i + 1;
	}
}

method Main()
{
   var s:string:="Hell";
   var t:string:="Hello World";

   assert s[..] == "Hell";
   assert t[..] == "Hello World";
   var r:bool:=isPrefix(s,t);
   // isPrefix works
   assert r;
}
