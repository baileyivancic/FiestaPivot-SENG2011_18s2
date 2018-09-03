predicate hasPrefix(token: string, str: string)
{
  |token| <= |str| && token == str[..|token|]
}

predicate hasSubstring(token:string, str:string)
{
	exists n :: 0 <= n < |str| && hasPrefix(token, str[n..])
}

predicate hasNoSubstring(token:string, str:string)
{
	forall n :: 0 <= n < |str| ==> !hasPrefix(token,str[n..])
}

method isPrefix(token: string, str: string) returns (r:bool)
  requires |token|>0 && |str|>0
	ensures r ==> hasPrefix(token,str)
	ensures !r ==> !hasPrefix(token,str)
{
  if (|str| < |token|) {
    r:=false;
  } else {
    r:=(str[..|token|] == token);
  }
}

method isSubstring(token: string, str: string) returns (r:bool)
  requires |token| <= |str| && |token|>0 && |str|>0
	ensures r ==> hasSubstring(token, str)
  ensures !r ==> hasNoSubstring(token, str)
{
  var m;
  var i := 0;
  r := false;

  while (i < |str| && r == false)
  	invariant 0 <= i <= |str|
  	invariant r ==> i>0 && hasPrefix(token, str[i-1..])
  	invariant !r ==> forall l :: 0 <= l < i ==> !hasPrefix(token, str[l..])
  	decreases |str| - i
  {
  	m := isPrefix(token, str[i..]);
  	if (m == true) {
  		r := true;
  	}
  	i := i + 1;
  }
}

//Testing (Sanity checks)
method Main() {
  var s:string:="ell";
  var t:string:="Hello World";

  print(t[1..1+|s|]);
}

method testPrefix()
{
  //Yes cases
  var s:string:="Hell";
  var t:string:="Hello World";

  assert s[..] == "Hell";
  assert t[..] == "Hello World";
  var r:bool:=isPrefix(s,t);
  assert r;

  //No cases
  s:="ello";
  t:="Hello World";

  assert s[..] == "ello";
  assert t[..] == "Hello World";
  r:=isPrefix(s,t[1..]);
  assert r;
}

method testSubstring() {
  var t:string:="no";
  var s:string:="Hello World";

  assert t[..] == "no";
  assert s[..] == "Hello World";
  var r:bool:=isSubstring(t,s);
  //assert r;

  assert forall n :: ( 0 <= n < |s|-|t| +1) ==> t != s[n..n+|t|];
}
