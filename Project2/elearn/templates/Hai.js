function a(){
var x=document.getElementById("123");
var y=x.value;
console.log(y);
document.getElementById(y).style.backgroundColor="blue";}

document.addEventListener("keypress",a());