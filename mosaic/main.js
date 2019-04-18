var dotDiameter = 10;

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

var strokes = [];
var stroke = [];
var isPenDown = false;

// var img = new Image();
// img.addEventListener("load", function() {
//   ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, canvas.width, canvas.height);
// }, false);
// img.src = "../assets/paint-horse-running-in-field.jpg";


function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

/* DRAWING STROKES */
function redraw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (var i = 0; i < strokes.length; i++) {
    var s = strokes[i];
    for (var j = 1; j < s.length; j++) {
      drawLine(s[j - 1], s[j]);
    }
  }
}

function drawLine(startPoint, endPoint) {
  ctx.beginPath();
  ctx.moveTo(startPoint.x, startPoint.y);
  ctx.lineTo(endPoint.x, endPoint.y);
  ctx.strokeStyle = "black";
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.closePath();
}

/* STORING STROKES */
canvas.addEventListener("mousedown", function(evt) {
  isPenDown = true;
  var mousePos = getMousePos(canvas, evt);
  stroke = [mousePos];
  strokes.push(stroke);
  redraw();
});

canvas.addEventListener("mousemove", function(evt) {
  if (isPenDown === true) {
    var mousePos = getMousePos(canvas, evt);
    stroke.push(mousePos);
    redraw();
  }
});

function endStroke(evt) {
  if (stroke.length > 0) {
    undoButton.removeAttribute("disabled");
  }
  isPenDown = false;
  redraw();
}
canvas.addEventListener("mouseup", endStroke);
canvas.addEventListener("mouseleave", endStroke);

/* UNDO BUTTON */
var undoButton = document.getElementById("undo");
undoButton.addEventListener("click", function() {
  if (strokes.length > 0) {
    strokes.pop();
  }
  if (strokes.length <= 0) {
    undoButton.setAttribute("disabled", "");
  }
  redraw();
});
