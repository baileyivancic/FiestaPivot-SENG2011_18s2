// Sources: https://github.com/Microsoft/dafny/blob/master/Test/dafny0/LiberalEquality.dfy
// https://github.com/Microsoft/dafny/issues/191 (Zero Initialisers <(Data(0)>))
// https://gist.github.com/palmskog/04673cef891e09732b0540c8578aa5de
// Max Capacity of ArrayList = 1000
// Generic Datatype used. Quicksort is abstracted from our custom arraylist as Dafny makes it difficult to do multiple comparisons of
// datatypes.
// This class is fully verified and is only used in the project as a proof of concept for the overall big picture.

class ArrayList<Data(0)> {

    var arr: array<Data>;
    var len: int;
    ghost var seqList: seq<Data>;
    ghost var repr: set<object>;

    predicate Valid()
      reads this, repr;
    {
      (repr == {this, arr}) && |seqList| == len && len <= arr.Length &&
      (forall i | 0 <= i < len :: arr[i] == seqList[i])
    }

    // Fresh Usage here: https://github.com/Microsoft/dafny/wiki/FAQ
    constructor()
      ensures Valid() 
      ensures fresh(repr - {this})
      ensures len == 0;
      ensures seqList == [];
      ensures arr.Length == 1000;
    {
      len := 0;
      seqList := [];
      arr := new Data[1000];
      repr := {this} + {arr};
    }

    method length() returns (res: int)
      requires Valid();
      ensures Valid();
      ensures res == |seqList|;
    {
      res := len;
    }

    method isEmpty() returns (res: bool)
      requires Valid();
      ensures Valid()
      ensures res <==> (|seqList| == 0);
    {
      res := (len == 0);
    }

    method get(counter: int) returns (res: Data)
      requires Valid()
      requires 0 <= counter < len;
      ensures Valid();
      ensures res == seqList[counter];
    {
      res := arr[counter];
    }

    method remove(counter: int)
      modifies repr;
      requires Valid() 
      requires counter >= 0 && counter < len;
      ensures Valid();
      ensures len == old(len) - 1;
      ensures seqList == old(seqList[0..counter]) + old(seqList[counter + 1..len]);
      ensures forall k | 0 <= k < counter :: (seqList[k] == old(seqList[k]));
      ensures forall k | counter <= k < len :: (seqList[k] == old(seqList[k + 1]));
      ensures repr == old(repr);
    {
      ghost var l := seqList[0..counter];
      var i := counter;
      while (i < len - 1)
        modifies arr;
        invariant counter <= i < len;
        invariant |l| == i;
        invariant l == seqList[0..counter] + seqList[counter + 1..i + 1];
        invariant forall j | (counter <= j < i) :: (arr[j] == old(arr[j+1]));
        invariant forall j | (0 <= j < i) :: (arr[j] == l[j]);
        invariant forall j | (i < j < arr.Length) :: (arr[j] == old(arr[j]));
      {
        arr[i] := arr[i+1];
        l := l + [arr[i]];
        i := i + 1;
      }
      seqList := l;
      len := len - 1;
    }

    method add(element: Data) returns (counter: int)
      modifies repr;
      requires Valid();
      ensures Valid();
      ensures len == old(len) + 1;
      ensures counter == old(len);
      ensures seqList[counter] == element;
      ensures seqList == old(seqList) + [element];
      ensures forall k | (0 <= k < counter) :: (seqList[k] == old(seqList[k]));
      ensures (old(arr.Length) < old(len) + 1) ==> (fresh(repr - {this}) && arr.Length >= old(len) + 1);
      ensures (old(arr.Length) >= old(len) + 1) ==> (repr == old(repr));
    {
      ensureCapacity(len + 1);
      arr[len] := element;
      seqList := seqList + [element];
      counter := len;
      len := len + 1;
    }

    // Source: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/krml203.pdf
    // Usage of fresh(repr - {this}) as explained in Section 1.5
    method ensureCapacity(minCapacity: int)
      modifies repr;
      requires Valid();
      ensures Valid() 
      ensures seqList == old(seqList);
      ensures minCapacity > old(arr.Length) ==> fresh(repr - {this});
      ensures minCapacity <= old(arr.Length) ==> repr == old(repr);
      ensures arr.Length >= minCapacity;
    {
      var oldCapacity := arr.Length;
      if minCapacity > oldCapacity {
        var newCapacity := (oldCapacity * 3)/2 + 1;
        if (newCapacity < minCapacity) {
          newCapacity := minCapacity;
        }
        var newArr := new Data[newCapacity];
        duplicate(arr, 0, newArr, 0, len);
        repr := repr - {arr} + {newArr};
        arr := newArr;
      }
    }

    method append(a: ArrayList<Data>)
      modifies repr;
      requires Valid()
      requires a.Valid() 
      requires repr !! a.repr;
      ensures Valid();
      ensures len == old(len) + a.len;
      ensures seqList == old(seqList) + a.seqList;
      ensures forall k :: 0 <= k < old(len) ==> seqList[k] == old(seqList[k]);
      ensures forall k :: 0 <= k < a.len ==> seqList[old(len) + k] == a.seqList[k];
      ensures old(arr.Length) < old(len) + a.len ==> fresh(repr - {this});
      ensures old(arr.Length) >= old(len) + a.len ==> repr == old(repr);
    {
      var numNew := a.len;
      ensureCapacity(len + numNew);
      duplicate(a.arr, 0, arr, len, numNew);
      seqList := seqList + a.seqList;
      len := len + numNew;
    }

}

method duplicate<Data>(src:array<Data>, start:int, dst:array<Data>, end:int, len:int)
  modifies dst;
  requires src != dst;
  requires 0 <= len;
  requires 0 <= start && start + len <= src.Length;
  requires 0 <= end && end + len <= dst.Length;
  ensures forall k :: 0 <= k < end ==> dst[k] == old(dst[k]);
  ensures forall k :: end <= k < end + len ==> dst[k] == src[k - end + start];
  ensures forall k :: end + len <= k < dst.Length ==> dst[k] == old(dst[k]);
  ensures forall k :: start <= k < start + len ==> src[k] == dst[k - start + end];
{
  var i := 0;
  while (i < len)
    invariant 0 <= end && end + i <= dst.Length;
    invariant 0 <= start && start + i <= src.Length;
    invariant forall k :: 0 <= k < end ==> dst[k] == old(dst[k]);
    invariant forall k :: end <= k < end + i ==> dst[k] == src[k - end + start];
    invariant forall k :: end + len <= k < dst.Length ==> dst[k] == old(dst[k]);
  {
    dst[end + i]  := src[start + i];
    i := i + 1;
  }
}

