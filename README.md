# Crowd Art

For our final project for NETS 213 - Crowdsourcing and Human Computation, we are exploring various approaches to create art using Mechanical Turk workers. We have devised of four experiments that each generate art in different ways.

## Experiments

### Pointillism

The output of the Pointillism subproject will be an image that is colored using only dots (in the style of Pointillism). The HIT will consist of a source image on the side, and the Turkers will be able to pick a color from a limited palette of our choosing and place a dot on the canvas in that color. The creation of the art will be done iteratively, with each Turker putting down between 10 and 20 dots, until the picture is complete. (We plan on restricting the placement of dots to points on a grid so that once the entire grid is filled we can declare the art completed.) Each Turker will see all the dots that have been previously placed when placing their own dots.

### Mosaic

The output of the Mosaic subproject will be a human-drawn outline of an image. To facilitate this, we are going to divide up an image into many sections. Each section will be sketched by a crowd worker. After all the sections are sketched, we will put them back together in the same order as in the source image. Given that each section is drawn by a different worker, it is likely that not all the sections will fit perfectly together and each section might be drawn in a different style. This is intended, since it will make the sketch more artistically interesting and give it a mosaic aesthetic.

### From clicks comes form

The output of the Clicks subproject will be a heatmap of sorts showing where people click on an image. We will provide Turkers with a source image, say of a horse galloping in a field, and tell all of them to click on anywhere they want within a specific part of the image, say the horse. Our hypothesis is that some Turkers will click on the head of the horse, while others might click on the horses main, while others might click on the tail, while still others might click on other parts of the horse. The result will be a bunch of dots that approximate the shape of a horse.

## Quality Control

Due to the inherent subjectivity of art, we plan on imposing weak quality control in the experiments above (this was suggested and approved by Professor Callison-Burch). Since in all cases, each Turker is only contributing a small amount to the final piece of artwork, we believe that even a small deviance in quality will not have a significant effect on the final product. Furthermore, we plan on using strategic compensation strategies to incentivize the Turkers to perform the tasks well (see the section about evaluation below).

## Evaluation

We plan on running each of these experiments multiple times. As a second layer of crowd sourcing, we will ask the Turkers to rank which piece of artwork they like best within each experiment and then overall. We are considering paying a bonus to every Turker who contributed to the winning artwork (pending financial feasibility).
