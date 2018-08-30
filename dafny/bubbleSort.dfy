// http://www.cse.unsw.edu.au/~se2011/2014Material/Week03/Sorting.pdf
// http://soe.rutgers.edu/sites/default/files/imce/pdfs/gset-2014/Formal%20Verification%20with%20Dafny.pdf
// SENG2011
// Harry Tang
// Basic Bubble Sort for IDs

predicate SortedUpTo(a:array<int>,lower:int,upper:int)
  requires 0 <= upper <= a.Length;
  reads a;
{
  forall j,k :: 0 <= j < k < upper ==> a[j] <= a[k]
}

method BubbleSort(a:array<int>)
  requires a.Length > 1;
  modifies a;
  ensures SortedUpTo(a,a.Length);
{
  var i := a.Length -1;
  var upperBound := 0;
  while(upperBound < a.Length)
    invariant 0 <= upperBound <= a.Length; // filler
    invariant forall j,k :: 0 <= j < upperBound && upperBound <= k < a.Length ==> a[j] <= a[k]; // same
    invariant SortedUpTo(a,upperBound); // same
  {
    i := a.Length - 1;
    while(i > upperBound)
      invariant upperBound <= i < a.Length;
      invariant forall j :: i <= j < a.Length ==> a[i] <= a[j]; // with every iteration, the max(a[i..upper]) moves to the 'end'
      invariant forall j,k :: 0 <= j < upperBound && upperBound <= k < a.Length ==> a[j] <= a[k]; // since all the larger elements are moving to the end, if you partition the array with the upper bound, all elements in a[k] are larger than a[j]
      invariant SortedUpTo(a,upperBound); // growing sort for each iteration
      decreases i; // filler
    {
      if (a[i-1] >= a[i])
      {
        a[i],a[i-1] := a[i-1],a[i];
      }
      i := i-1;
    }
    upperBound := upperBound + 1;
  }
}

method Test()
{
  var a:array<int>:= new int[][1,4,3,2,5];
  assert a[0] == 1;
  assert a[1] == 4;
  assert a[2] == 3;
  assert a[3] == 2;
  assert a[4] == 5;
  assert SortedUpTo(a,a.Length) == false;
  BubbleSort(a);
  assert SortedUpTo(a,a.Length) == true;

}
