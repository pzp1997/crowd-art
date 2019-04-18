# Crowd Art

For our final project for NETS 213 - Crowdsourcing and Human Computation, we are exploring various approaches to create art using Mechanical Turk workers. We have devised of four experiments that each generate art in different ways.

## Experiments

### Pointillism

The output of the Pointillism subproject will be an image that is colored using only dots (in the style of Pointillism). The HIT will consist of a source image on the side, and the Turkers will be able to pick a color from a limited palette of our choosing and place a dot on the canvas in that color. The creation of the art will be done iteratively, with each Turker putting down between 10 and 20 dots, until the picture is complete. (We plan on restricting the placement of dots to points on a grid so that once the entire grid is filled we can declare the art completed.) Each Turker will see all the dots that have been previously placed when placing their own dots. 
Overall amount of work: 8 points
-Webapp for placing dots (JavaScript): 3
-Sequential Processing of HITS: 4+
-HIT design and management: 1

### Mosaic

The output of the Mosaic subproject will be a human-drawn outline of an image. To facilitate this, we are going to divide up an image into many sections. Each section will be sketched by a crowd worker. After all the sections are sketched, we will put them back together in the same order as in the source image. Given that each section is drawn by a different worker, it is likely that not all the sections will fit perfectly together and each section might be drawn in a different style. This is intended, since it will make the sketch more artistically interesting and give it a mosaic aesthetic.
Overall amount of work: 8 points
-Webapp specific for Turkers to draw the fragments: 3
-Script to segment the image: 2
-Script to put image back together at the end: 2
-HIT design and management: 1

### From clicks comes form

The output of the Clicks subproject will be a heatmap of sorts showing where people click on an image. We will provide Turkers with a source image, say of a horse galloping in a field, and tell all of them to click on anywhere they want within a specific part of the image, say the horse. Our hypothesis is that some Turkers will click on the head of the horse, while others might click on the horse's mane, while others might click on the tail, while still others might click on other parts of the horse. The result will be a bunch of dots that approximate the shape of a horse.
Overall difficulty ranking: 3 points
-Webapp specific to this task: 2
-HIT design and management: 1

## Quality Control

Due to the inherent subjectivity of art, we plan on imposing weak quality control in the experiments above (this was suggested and approved by Professor Callison-Burch). Since in all cases, each Turker is only contributing a small amount to the final piece of artwork, we believe that even a small deviance in quality will not have a significant effect on the final product. Furthermore, we plan on using strategic compensation strategies to incentivize the Turkers to perform the tasks well (see the section about evaluation below).

## Evaluation

We plan on running each of these experiments multiple times. As a second layer of crowd-sourcing, we will ask the Turkers to rank which piece of artwork they like best within each experiment and then overall. We are considering paying a bonus to every Turker who contributed to the winning artwork (pending financial feasibility). The total expected amount of work is 19 points.  

## Data

Our input data mainly consists of a single image of a horse.  This can be found in the "assets" folder of our project (‘paint-horse-running-in-field').  

For the pointillism task, users will be given this image, which will be located below a canvas,  along with an empty (or partially-completed) canvas to add 10 dots to, trying to recreate the horse image, so the input data will just be the image. The output of a single workers efforts will be a picture with 10 more dots than the image he received and hopefully an image that more closely resembles the given image. If the worker is the final worker then the output will be the completed pointillism image.  An example of our what the output will look like can be found in the ‘samples/’ directory (‘pointillism.png’).

We have a working web application for the pointillism portion of the project in our ‘src/pointillism/’ directory.  We encourage you to try our demo pointillism application: http://palmerpaul.com/crowd-art/pointillism/. We still, however, need to add code to take results from previous Turkers’ tasks and feed them as input to our next batch of workers.  We may need to do this manually, as we still haven't found a way to automatically take care of the chaining process.

For the HeatMap task, where users will click on different areas in the horse image, the users will just need the image as input. The output data of each worker will be the list of x,y coordinates of that worker’s 10 dots. This will be entered into a master CSV. Our sample CSV for this assignment is titled ‘heatmap_sample_csv’ and can be found in the ‘samples/’ directory.  An example of the finished product can be found in ‘samples/’ (horse_heatmap_example.jpg’).

We have a working web application for our Heat Map tasks as well. We encourage you to try out our demo application for the HeatMap module: http://palmerpaul.com/crowd-art/heatmap/. As this task does not require workers to build iteratively off of previous workers’ work, the only additional functionality to add is creating a new image from the points in the master CSV.

For the mosaic task, the image needs to be split up, so the input would be a section of the image. In the ‘mosaic/scripts’ folder, we have a script to divide the images into any number of pieces, as well as actual sample images that we divided using our script.  After we publish the tasks, we will collect the result images from Turk and use our image combiner (also in ‘mosaic/scripts’) to reassemble the Turkers’ outlines of the image into a complete image.  A sample of what the output should look like can be found in the ‘samples/’ directory (‘horse-outline’).

As mentioned, we have working code to divide and combine images in ‘mosaic/scripts.’  We will weigh the tradeoffs of implementing the remainder of this module ourselves using HTML 5 canvas vs modifying Mechanical Turk’s outlining task format.

Regarding quality control, we have a sample HIT both for inter-category comparisons (pointillism vs. mosaic, for example) and intra-category comparisons (different pointillism images).  These can be found in the ‘samples/’ directory as ‘example_hit_inter’ and ‘example_hit_intra’.  The output will be a batch CSV similar to the ones we’ve seen in previous assignments.  An example of this can be found in ‘samples/’ as well (‘sampleOutputQualityControl(Batch).csv’).  We have code in our ‘src/’ directory (‘eval.ipynb’) to analyze this data and determine which the most desirable images and methodology for creating these images.

After discussing ways to improve our quality control module with Professor Callison-Burch, we plan on adding additional features such as (1) a check to make sure that the pointillism Turkers clicked at least a certain number of points and (2) a check to see if Turkers in the heatmap task are placing all of their points within the general boundaries of the point of interest in the image (the horse or element in background).  We may choose to evaluate criterion (2) manually by visualizing the dots on the image and looking for outliers or by writing a script that incorporates outlining of the horse by Turkers.


