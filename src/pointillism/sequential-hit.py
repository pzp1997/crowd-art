import boto3
import datetime

# Use the Amazon Mechanical Turk Sandbox to publish test Human Intelligence Tasks (HITs) without paying any money.
# Use this endpoint_url instead to use production
# endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
)

question_template = (
"""<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
  <HTMLContent><![CDATA[
<!-- You must include this JavaScript file -->
<script src="https://assets.crowd.aws/crowd-html-elements.js"></script>

<!-- For the full list of available Crowd HTML Elements and their input/output documentation,
      please refer to https://docs.aws.amazon.com/sagemaker/latest/dg/sms-ui-template-reference.html -->

<!-- You must include crowd-form so that your task submits answers to MTurk -->
<crowd-form answer-format="flatten-objects">

  <crowd-instructions link-text="View instructions" link-type="button">
    <short-summary>
      <p>
        In the bottom-right corner is an image of a horse. We are trying to
        recreate this image using colored dots. Use the color picker (below the
        canvas on the left) to choose a color and click on the canvas to add
        dots. You must add exactly 20 dots to submit the HIT.
      </p>
    </short-summary>

    <detailed-instructions>
      <p>
        If you make a mistake, clicking on the undo button will remove the
        most recently placed dot.
      </p>
      <p>
        We will give a bonus to all workers who contributed to the "best"
        picture from all the iterations of this HIT group. If you submit
        low-quality work, your picture will have a worse chance of being
        selected.
      </p>
    </detailed-instructions>

    <!-- <positive-example>
      <p>Provide an example of a good answer here</p>
      <p>Explain why it's a good answer</p>
    </positive-example> -->

    <!-- <negative-example>
      <p>Provide an example of a bad answer here</p>
      <p>Explain why it's a bad answer</p>
    </negative-example> -->
  </crowd-instructions>

  <style>
    /* Source: Bootstrap 4.2.1 */
    /* BEGIN BOOTSTRAP */
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      color: #212529;
      text-align: left;
      background-color: #fff;
    }
    .container {
      /* width: 100%; */
      padding-right: 15px;
      padding-left: 15px;
      margin-right: auto;
      margin-left: auto;
    }
    .btn {
      display: inline-block;
      font-weight: 400;
      color: #212529;
      text-align: center;
      vertical-align: middle;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
      background-color: transparent;
      border: 1px solid transparent;
      padding: 0.375rem 0.75rem;
      font-size: 1rem;
      line-height: 1.5;
      border-radius: 0.25rem;
      transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }
    .btn-light {
      color: #212529;
      background-color: #f8f9fa;
      border-color: #f8f9fa;
    }

    .btn-light:hover {
      color: #212529;
      background-color: #e2e6ea;
      border-color: #dae0e5;
    }

    .btn-light:focus, .btn-light.focus {
      box-shadow: 0 0 0 0.2rem rgba(216, 217, 219, 0.5);
    }

    .btn-light.disabled, .btn-light:disabled {
      color: #212529;
      background-color: #f8f9fa;
      border-color: #f8f9fa;
    }
    button {
      border-radius: 0;
    }

    button:focus {
      outline: 1px dotted;
      outline: 5px auto -webkit-focus-ring-color;
    }

    input,
    button,
    select,
    optgroup,
    textarea {
      margin: 0;
      font-family: inherit;
      font-size: inherit;
      line-height: inherit;
    }

    button,
    input {
      overflow: visible;
    }

    button,
    select {
      text-transform: none;
    }
    .text-center {
      text-align: center !important;
    }
    .float-left {
      float: left !important;
    }
    .float-right {
      float: right !important;
    }
    .clearfix::after {
      display: block;
      clear: both;
      content: "";
    }
    .pt-3 {
      padding-top: 1rem !important;
    }
    /* END BOOTSTRAP */

    body {
      background-color: #333;
    }
    #canvas {
      border: 1px solid black;
      margin-top: 20px;
    }
    .toolbar {
      margin: 0 auto;
    }
    .dot {
      display: inline-block;
      height: 31px;
      width: 31px;
      border-radius: 50%;
      margin: 0 3px;
    }
    .color-option-selected {
      height: 25px;
      width: 25px;
      border: 3px solid white;
    }

  </style>

  <div class="container text-center">
    <canvas id="canvas"></canvas>
    <div class="toolbar">
      <div id="color-selector" class="float-left"></div>
      <div class="float-right">
        <button id="undo" class="btn btn-light" disabled>Undo</button>
      </div>
      <div class="clearfix"></div>
    </div>
    <div class="toolbar pt-3">
      <div class="float-right">
        <img src="http://palmerpaul.com/crowd-art/src/assets/horse.jpg" width="220px" alt="horse">
      </div>
    </div>
  </div>

  <crowd-input id="response" name="response" type="hidden" style="display:hidden;"></crowd-input>
  <crowd-button id="submitButton" form-action="submit" variant="primary" disabled>Submit</crowd-button>

  <script type="text/javascript">
  document.addEventListener("DOMContentLoaded", function(event) {
    /* CONSTANTS */
    var pictureWidth = 60;
    var pictureHeight = 40;
    var dotDiameter = 10;
    var dotsPerHit = 20;
    var colors = ["red", "blue", "yellow", "orange", "green", "purple", "brown", "black", "white"];

    /* STATE */
    var selectedColor = colors[0];
    var existingDots = JSON.parse(${data});
    var dots = [];
    var countNewDots = 0;

    /* CANVAS SETUP */
    var canvas = document.getElementById("canvas");
    canvas.width = pictureWidth * dotDiameter;
    canvas.height = pictureHeight * dotDiameter;

    var toolbars = document.getElementsByClassName("toolbar");
    for (var i = 0; i < toolbars.length; i++) {
      toolbars[i].style.width = (pictureWidth * dotDiameter) + "px";
    }

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
      if (countNewDots >= dotsPerHit) {
        return;
      }

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
      if (countNewDots >= dotsPerHit) {
        return;
      }

      var mousePos = getMousePos(canvas, evt);
      var col = Math.floor(mousePos.x / dotDiameter);
      var row = Math.floor(mousePos.y / dotDiameter);

      if (!dotAtPosition(row, col)) {
        dots.push({
          c: col,
          r: row,
          color: selectedColor,
          timestamp: Date.now(),
        });
        countNewDots++;
        if (countNewDots >= dotsPerHit) {
          submitButton.removeAttribute("disabled");
        }
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

    /* SUBMIT RESPONSE TO MTURK */
    var submitButton = document.getElementById("submitButton");
    var response = document.getElementById("response");
    submitButton.addEventListener("click", function() {
      response.value = JSON.stringify(existingDots.concat(dots));
    });
  });
  </script>
</crowd-form>

]]>
  </HTMLContent>
</HTMLQuestion>
""")

# Create the HIT
response = client.create_hit(
    MaxAssignments = 1000,
    LifetimeInSeconds = int(datetime.timedelta(days=7).total_seconds()),
    AssignmentDurationInSeconds = int(datetime.timedelta(hours=1).total_seconds()),
    Reward ='0.05',
    Title = 'Add 20 colored dots to a canvas to recreate image of a horse',
    Keywords = 'click,dots,color,horse',
    Description = 'We are trying to recreate an image of a horse using colored dots. Use the color picker to choose a color and click on the canvas to add dots. You must add exactly 20 dots to submit the HIT. Bonus will be paid to best picture!',
    Question = question_template,
    HITLayoutParameters = [{'Name': 'data', 'Value': '[]'}],
)

# The response included the HITTypeId, which we'll use to configure your Notifications
hit_type_id = response['HIT']['HITTypeId']
print(hit_type_id)

# Your SNS Topic - create or get it at https://console.aws.amazon.com/sns/v2/home?region=us-east-1#/topics
# Example: 'arn:aws:sns:us-east-1:123456789012:MTurk-SNS'
sns_topic = 'arn:aws:sns:us-east-1:277402979440:mturk-sns-test'

# Configure the Notification structure using the SNS Topic ARN
# to which you'd like MTurk to publish Notifications
notification = {
    'Destination': sns_topic,
    'Transport': 'SNS',
    'Version': '2014-08-15',
    'EventTypes': ['AssignmentSubmitted']
}

# Configure Notification settings using the HITTypeId for which
# you'd like to receive Notifications
client.update_notification_settings(
    HITTypeId = hit_type_id,
    Notification = notification,
)
