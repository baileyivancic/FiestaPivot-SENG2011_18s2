// Incomplete & Not Working

predicate isOdd(src:int)
{
  src%2 == 0
}

method filter(src:array<int>, p:predicate) returns (dst:array<int>, n: nat)
  requires src != null;
  ensures dst != null;
  ensures dst.Length <= src.Length;
  ensures forall k :: 0 <= k < n ==> p(dst[k]);  
  ensures forall j :: 0 <= j < n ==> dst[j] in src[..];
  ensures forall k :: 0 <= k < src.Length && p(src[k]) ==> exists j:: 0 <= j < n && dst[j] == src[k] ;    
{
  dst := new int[src.Length];
  n := 0;
  var i := 0;

  while (i < src.Length)
    invariant n <= i <= src.Length;
    invariant n <= dst.Length;
    invariant forall k :: 0 <= k < n ==> p(dst[k]) ;
    invariant forall j :: 0 <= j < n ==> dst[j] in src[..i] ;
    invariant forall k :: 0 <= k < i && p(src[k]) ==> exists j:: 0 <= j < n && dst[j] == src[k] ;  
  {
    if p(src[i])
    { 
      dst[n] := src[i];
      n := n + 1;
    }
    i := i + 1;
  }
}
