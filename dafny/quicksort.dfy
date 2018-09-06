// method quicksort(a :array<int>, left: int, right:int)

// {
// 	if ( left < high ) {
// 		pivot = partition(a, left, right);
// 		quicksort(a, left, pivot-1);
// 		quicksort(a, pivot+1, right);
// 	}
// }

// method partition( a: array<int>, left: int, right: int) returns (p: int)

// {
//   j := left;
//   greater := left;
// 	pivot := a[right];

//   while ( j<=right ) 
  
//   {
//     if ( a[j] <= pivot ) {
//       greater := greater+1;
//       swap_elements(a, greater, j);
//     }
    
//     j := j+1;
//   }
//   swap_elements(a, greater, j);
//   return greater+1;
// }

method swap_elements(  a: array<int>, index1: int, index2: int) 
ensures a[index1] == old(a[index2]) && a[index2] == old(a[index1])
ensures forall i :: ( 0<=i<a.Length && i!=index1 && i!=index2) ==> a[i] == old(a[i])
{
	temp := 0;

	temp := a[index2];
	a[index2] := a[index1];
	a[index1] := temp;
}
