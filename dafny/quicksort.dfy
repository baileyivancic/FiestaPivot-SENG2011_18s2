method partition( a: array<int>, left: int, right: int) returns (greater: int)
modifies a
requires 0<=left<right<a.Length
ensures multiset(a[left..right]) == multiset(old(a[left..right]))
ensures left<=greater<=right
ensures forall i :: left<=i<=greater ==> a[i]<=a[greater]
ensures greater<right ==> ( forall i :: greater<i<=right ==> a[i]>a[greater] )
{
	var j := left;
	greater := left-1;
	var pivot := a[right];

	while ( j<=right ) 
	decreases right-j
	invariant left<=j<=right+1
	invariant left-1<=greater<j
	invariant forall i :: left<=i<=greater ==> a[i]<=pivot
	invariant forall i :: greater<i<j ==> a[i]>pivot
	{
		if ( a[j] <= pivot) {
			greater := greater+1;
			swap_elements(a, greater, j);
		}

		j := j+1;
	}

	assert greater<a.Length;
	assert pivot == a[greater];

	return greater;
}

// method quicksort(a :array<int>, left: int, right:int)

// {
// 	if ( left < right ) {
// 		pivot = partition(a, left, right);
// 		quicksort(a, left, pivot-1);
// 		quicksort(a, pivot+1, right);
// 	}
// }

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