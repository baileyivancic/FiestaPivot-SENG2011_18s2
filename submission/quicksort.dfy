// References:
// Microsoft's Verification Corner: The Dutch National Flag Algorithm (https://www.youtube.com/watch?v=dQC5m-GZYbk)
// Carroll Morgan's http://www.cse.unsw.edu.au/~se2011/2014Material/Week03/Sorting.pdf
// https://soe.rutgers.edu/sites/default/files/imce/pdfs/gset-2014/Formal%20Verification%20with%20Dafny.pdf

predicate sorted(a:array<int>, left:int, right:int)
	requires 0 <= left <= right <= a.Length
	reads a
{
	forall j,k | left <= j < k < right :: (a[j] <= a[k])
}
  
method quicksort(a: array<int>, left: int, right: int)
	decreases right - left
	requires a.Length > 0
	requires 0 <= left <= right <= a.Length
	requires (forall i | left <= i < right :: a[i] < a[right]) <== (0 <= left <= right < a.Length)
	requires (forall i | left <= i < right :: a[left - 1] <= a[i]) <== (0 < left <= right <= a.Length)
	ensures forall i | (0 <= i < left || right <= i < a.Length) :: (old(a[i]) == a[i])
	ensures (forall i | left <= i < right :: a[i] < a[right]) <== (0 <= left <= right < a.Length)
	ensures (forall i | left <= i < right :: a[left - 1] <= a[i]) <== (0 < left <= right <= a.Length)
	ensures sorted(a, left, right);
	// ensures multiset(a[..]) == multiset(old(a[..]))
	modifies a
{
	if(left < right-1)
	{
		var p := partition(a, left, right);
		quicksort(a, left, p);
		quicksort(a, p+1, right);
	}
}

method partition(a: array<int>, left: int, right: int) returns (p: int)
	requires a.Length > 0
	requires 0 <= left < right <= a.Length
	requires (forall i | left <= i < right :: (a[i] < a[right])) <== (0 <= left <= right < a.Length)
	requires (forall i | left <= i < right :: (a[left-1] <= a[i])) <== (0 < left <= right <= a.Length)
	ensures 0 <= left <= p < right <= a.Length
	ensures forall i | (left <= i < p) :: (a[i] < a[p])
	ensures forall i | (p < i < right) :: (a[p] <= a[i])
	ensures forall i | (0 <= i < left || right <= i < a.Length) :: (old(a[i]) == a[i])
	ensures (forall i | left <= i < right :: (a[i] < a[right])) <== (0 <= left <= right < a.Length)
	ensures (forall i | left <= i < right :: (a[left-1] <= a[i])) <== (0 < left <= right <= a.Length)
	// ensures multiset(a[..]) == multiset(old(a[..]))
	modifies a
{

	p := left;
	var k := left+1;

	while(k < right)
	decreases right - k
	invariant left <= p < k <= right
	invariant forall i | left <= i < p :: a[i] < a[p]
	invariant forall i | p < i < k :: a[p] <= a[i]
	invariant forall i | (0 <= i < left || right <= i < a.Length) :: (old(a[i]) == a[i])
	invariant (forall i | left <= i < right :: a[i] < a[right]) <== (0 <= left <= right < a.Length)
	invariant (forall i :: left <= i < right ==> a[left-1] <= a[i]) <== (0 < left <= right <= a.Length)
	// invariant multiset(a[..]) == multiset(old(a[..]))
	{
		if(a[k] < a[p])
		{
			var j := k-1;
			var tmp := a[k];
			a[k] := a[j];

			while(j > p)
			decreases j - p
			invariant a[p] > tmp
			invariant forall i | left <= i < p :: (a[i] < a[p])
			invariant forall i | p < i < k + 1 :: (a[p] <= a[i])
			invariant forall i | (0 <= i < left || right <= i < a.Length) :: (old(a[i]) == a[i])
			invariant (forall i :: left <= i < right ==> a[i] < a[right]) <== (0 <= left <= right < a.Length)
			invariant (forall i :: left <= i < right ==> a[left-1] <= a[i]) <== (0 < left <= right <= a.Length)
			// invariant multiset(a[..]) == multiset(old(a[..]))
			{
				a[j+1] := a[j];
				j := j-1;
			}
			
			a[p+1] := a[p];
			p := p+1;
			a[p-1] := tmp;
		}
		k := k+1;
	}
}

method test()
{
	var a:array<int>:= new int[][5,4,3,2,1];
	assert a[0] == 5;
	assert a[1] == 4; 
	assert a[2] == 3; 
	assert a[3] == 2; 
	assert a[4] == 1; 

	quicksort(a,0,a.Length);
	assert sorted(a,0,a.Length);
}
