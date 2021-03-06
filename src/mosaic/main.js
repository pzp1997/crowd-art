/* STATE */
var strokes = [];
var stroke = [];
var isPenDown = false;

/* CANVAS SETUP */
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top,
    timestamp: Date.now(),
  };
}

/* DRAWING STROKES */
function redraw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (var i = 0; i < strokes.length; i++) {
    if (strokes[i].undoTimestamp === null) {
      var s = strokes[i].data;
      for (var j = 1; j < s.length; j++) {
        drawLine(s[j - 1], s[j]);
      }
    }
  }
}

function drawLine(startPoint, endPoint) {
  ctx.beginPath();
  ctx.moveTo(startPoint.x, startPoint.y);
  ctx.lineTo(endPoint.x, endPoint.y);
  ctx.strokeStyle = "red";
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.closePath();
}

/* STORING STROKES */
canvas.addEventListener("mousedown", function(evt) {
  isPenDown = true;
  var mousePos = getMousePos(canvas, evt);
  stroke = [mousePos];
  strokes.push({
    data: stroke,
    undoTimestamp: null,
  });
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
  var i = strokes.length - 1;
  for (; i >= 0; i--) {
    if (strokes[i].undoTimestamp === null) {
      strokes[i].undoTimestamp = Date.now();
      break;
    }
  }
  if (i <= 0) {
    undoButton.setAttribute("disabled", "");
  }
  redraw();
});
