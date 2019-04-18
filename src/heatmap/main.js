var dotDiameter = 10;

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

var clicks = [];

function drawDot(x, y, color) {
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.arc(x, y, dotDiameter, 0, 2 * Math.PI);
  ctx.fill();
}

function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

canvas.addEventListener("click", function(evt) {
  var mousePos = getMousePos(canvas, evt);
  drawDot(mousePos.x, mousePos.y, "red");
  clicks.push(mousePos);
});
