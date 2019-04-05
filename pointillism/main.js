/* CONSTANTS */
var pictureWidth = 60;
var pictureHeight = 40;
var dotDiameter = 10;
var colors = ["red", "blue", "yellow", "orange", "green", "purple", "brown", "black", "white"];

/* STATE */
var selectedColor = colors[0];
var dots = [];
var countNewDots = 0;

/* CANVAS SETUP */
var canvas = document.getElementById("canvas");
canvas.width = pictureWidth * dotDiameter;
canvas.height = pictureHeight * dotDiameter;

document.getElementById("toolbar").style.width = (pictureWidth * dotDiameter) + "px";

var ctx = canvas.getContext("2d");
drawDots();

/* DRAWING */
function drawDot(x, y, color) {
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.arc(x, y, dotDiameter, 0, 2 * Math.PI);
  ctx.fill();
}

function drawDots() {
  var oldAlpha = ctx.globalAlpha;

  ctx.globalAlpha = 1;
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.globalAlpha = 0.75;
  for (var i = 0; i < dots.length; i++) {
    var dot = dots[i];

    drawDot(dot.c * dotDiameter, dot.r * dotDiameter, dot.color);
  }

  ctx.globalAlpha = oldAlpha;
}

function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

/* PREVIEW DOT */
canvas.addEventListener("mousemove", function(evt) {
  var mousePos = getMousePos(canvas, evt);
  var col = Math.floor(mousePos.x / dotDiameter);
  var row = Math.floor(mousePos.y / dotDiameter);

  drawDots();
  drawDot(col * dotDiameter, row * dotDiameter, selectedColor);
});

canvas.addEventListener("mouseleave", function(evt) {
  drawDots();
});

/* ADD DOT */
canvas.addEventListener("click", function(evt) {
  var mousePos = getMousePos(canvas, evt);
  var col = Math.floor(mousePos.x / dotDiameter);
  var row = Math.floor(mousePos.y / dotDiameter);

  if (!dotAtPosition(row, col)) {
    dots.push({
      c: col,
      r: row,
      color: selectedColor
    });
    countNewDots++;
    undoButton.removeAttribute("disabled");
    drawDots();
  }
});

function dotAtPosition(row, col) {
  for (var i = 0; i < dots.length; i++) {
    var dot = dots[i];
    if (dot.r === row && dot.c === col) {
      return dot;
    }
  }
  return null;
}

/* UNDO BUTTON */
var undoButton = document.getElementById("undo");
undoButton.addEventListener("click", function() {
  if (countNewDots > 0) {
    dots.pop();
    if (--countNewDots === 0) {
      undoButton.setAttribute("disabled", "");
    }
  }
  drawDots();
});

/* COLOR SELECTOR */
var SELECTED_CLASS = "color-option-selected";

function selectColorOption(color) {
  return function() {
    selectedColor = color;

    var selectedColorOptions = document.getElementsByClassName(SELECTED_CLASS);
    for (var i = 0; i < selectedColorOptions.length; i++) {
      selectedColorOptions[i].classList.remove(SELECTED_CLASS);
    }
    document.getElementById("option-" + color).classList.add(SELECTED_CLASS);
  };
}

var colorSelector = document.getElementById("color-selector");
for (var i = 0; i < colors.length; i++) {
  var color = colors[i];

  var colorOption = document.createElement("span");
  colorOption.id = "option-" + color;
  colorOption.classList.add("dot");
  if (color === selectedColor) {
    colorOption.classList.add(SELECTED_CLASS);
  }
  colorOption.style.backgroundColor = color;
  colorOption.addEventListener("click", selectColorOption(color));

  colorSelector.appendChild(colorOption);
}
