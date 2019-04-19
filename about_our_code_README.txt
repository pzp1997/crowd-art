Code explanation:

The code for all the HITs run by creating an HTML 5 canvas and allowing Turkers
to draw to it in various ways by capturing mouse events. We log some data about
how they are interacting with the application and encode the data as a JSON
string which we submit to the MTurk platform using a  hidden <crowd-input>.

The code for dividing and re-combining images for mosaic is a command-line
Python script that uses the Pillow library to read and manipulate image data.
The scripts accept flags to determine how many sections to divide the image into
and to figure out how many sections it needs to combine.

The sequential processing uses Amazon SNS as a pub/sub service to be notified
when a worker completes one of our HITs. When a notification occurs it triggers
an AWS Lambda function with some Python code that uses the boto3 client to
programmatically process the output from the last HIT and publish the next HIT
in the sequence.


Analysis:

To analyze our results, we will either post tasks to MTurk asking workers to
select the method of creation they like best by doing side-by-side image
comparison tasks, or we will use our own subjective opinions and those of our
friends to come to a consensus.  We will consider our project successful if
the crowd creates reasonable sound artwork.
