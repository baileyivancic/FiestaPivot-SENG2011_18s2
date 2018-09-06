method Main() {
  var a: array :=new int[][1, 2, 3, 6];
  var b: array := new int[][6, 2, 3, 1];
  
var inputA: array := new int[][5, 5, 5, -5, -5, -5];

  assert (a[0] == 1 && a[1] == 2 && a[2] == 3 && a[3] == 6);
  assert (b[0] == 6 && b[1] == 2 && b[2] == 3 && b[3] == 1); 
}