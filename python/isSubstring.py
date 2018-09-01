# method isSubstring(token: string, str: string) returns (r:bool)
#   requires |token| <= |str| && |token|>0 && |str|>0
# 	ensures r ==> hasSubstring(token, str)
#   ensures !r ==> hasNoSubstring(token, str)
# {
#   var m;
#   var i := 0;
#   r := false;

#   while (i < |str| && r == false)
#   	invariant 0 <= i <= |str|
#   	invariant r ==> i>0 && hasPrefix(token, str[i-1..])
#   	invariant !r ==> forall l :: 0 <= l < i ==> !hasPrefix(token, str[l..])
#   	decreases |str| - i
#   {
#   	m := isPrefix(token, str[i..]);
#   	if (m == true) {
#   		r := true;
#   	}
#   	i := i + 1;
#   }
# }