method partition( a: array<int>, left: int, right: int) returns (greater: int)
modifies a
ensures left==old(left) && right==old(right)
requires 0<=left<right<a.Length
ensures multiset(a[..]) == multiset(old(a[..]))
ensures left<=greater<=right
ensures forall i :: left<=i<=greater ==> a[i]<=a[greater]
ensures greater<right ==> ( forall i :: greater<i<=right ==> a[i]>a[greater] )
{
	var j := left;
	greater := left-1;
	var pivot := a[right];
	assert pivot == a[right];

	while ( j<right ) 
	decreases right-j
	invariant left<=j<=right
	invariant left-1<=greater<j
	invariant forall i :: left<=i<=greater ==> a[i]<=a[right]
	invariant forall i :: greater<i<j ==> a[i]>a[right]
	invariant multiset(a[..]) == multiset(old(a[..]))
	{
		if ( a[j] <= a[right] ) {
			greater := greater+1;
			swap_elements(a, greater, j);
		}

		j := j+1;
	}

	assert right == j;
	assert a[j]<=a[right];

	if ( a[j] <= a[right] ) {
		greater := greater+1;
		swap_elements(a, greater, j);
	}

	return greater;
}

method quicksort(a :array<int>, left: int, right:int)
decreases right-left
decreases right
modifies a 
requires 0<=left<a.Length &&  0<=right<a.Length
ensures multiset(a[..]) == multiset(old(a[..]))
{
	if ( left < right ) {
		var pivot := partition(a, left, right);
		quicksort(a, left, pivot-1);
		quicksort(a, pivot+1, right);
	}
}

method swap_elements(a: array<int>, index1: int, index2: int) 
modifies a
requires 0<=index1<a.Length && 0<=index2<a.Length
ensures a[index1] == old(a[index2]) && a[index2] == old(a[index1])
ensures multiset(a[..]) == multiset(old(a[..]))
ensures forall i :: ( 0<=i<a.Length && i!=index1 && i!=index2) ==> a[i] == old(a[i])
{
	var temp := 0;

	temp := a[index2];
	a[index2] := a[index1];
	a[index1] := temp;
}