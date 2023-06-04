# Ganz Interaction Zones (BETA)

## Overview
Unofficial interaction zones project for Talon Voice. Use your cursor to activate commands by hovering or clicking on zones. Design zones via an image creation program and use them in Talon. Report any bugs or enhancements.
![image showing interaction zones](http://ganeshsaraswat.ca/InternetImages/zones.gif)

## Features
* 2 types of zones: simple (similar to a button switch), trigger (similar to a lever switch).
* 2 interaction methods: clicking, hovering.
* Start delay and repeat command configuration options.
* Optional modifiers to customize the behaviour of zones.
* A small button to toggle zones on/off.

## Supported Commands/Actions
* Insert text [ex: hello world]
* Any key action supported by Talon (https://talon.wiki/key_action/) [ex: ctrl-s]
* Key bindings, requires (https://github.com/FireChickenProductivity/TalonKeyRebindings) [ex: bind: a,mouse 0, unbind: a]
* Swapping interaction zones [ex: swap: default]

## Workflow Overview
1. Draw your zones in your image editing program and use text boxes inside of the zones to configure them. Requires any image editing program that exports to PDF (https://www.photopea.com/ or Photoshop are examples). Every unique zone must have a unique colour (even a little difference is fine), all text for a particular zone must be within that unique colour.
2. Download pdf files to …/pdfparser/ subdirectory. Use the pdf_parser.py utility to automatically convert the PDF into a visual (.png stripped of text), and config file (.txt).
3. Use the interaction zones.

## Installation
1. Clone this repository into the Talon user folder.
3. First time users need to create an interaction zone. A default.pdf interaction zone is included in .../pdfparser/. You need to run the pdf_parser.py file in the .../pdfparser directory as a standalone script and select the "Parse Pdf" option in order to generate the interaction zone files. This requires the PyMuPDF (https://pypi.org/project/PyMuPDF/) library to be installed.
4. If required, you can use the same utility to resize the output of the PDFs to your local machines screen size using the "Resize All Images" option when running the utility.
5. Restart Talon and click the little grey rectangle in the top centre of your screen to toggle the zones on-and-off.

# Creating Custom Interaction Zones
Creating a custom interaction zone occurs inside of an image editing program such as Photopea (https://www.photopea.com/) or Photoshop.<br /><br />
You must define zones by using unique colours and then place configuration text inside of those zones.

### Example of Good Zone PDF
![example of good zone configuration](http://ganeshsaraswat.ca/InternetImages/zconfiguration.jpg)

## Creating the Zones PDF
For your reference these are the rules for when you're creating a custom interaction zone. Look at the example above for an intuitive understanding of how this works.
1. Every interaction zone must have a unique colour (as long as the colour is a little bit different, its fine).
2. All text (the configuration text) must be inside the appropriate unique colour.
3. The background of the exported PDF must be pure white.
3. All markings for zones must be pixel perfect. 
	1. This means that every pixel must be 100% the intended colour. Many image editing operations (rescaling, rotating, paint brushes etc.) will apply a little bit of blurring to the edges of your marks. This is currently not allowed.
	2. Use the pencil tool instead of brushes, disable feathering on selections, and turn the hardness and opacity to 100%. 
	3. A good method to check is to zoom in as far as you can onto the edges of your shapes and see if there's any blurring. You want no smooth transitions between colors.<br /><br />
Note: you must replace and regenerate the default.pdf to swap to custom zones.

### Configuration File Format
Title of the interaction zone<br />
on [click/hover] [trigger/NONE] [warmup/NONE] [repeat delay/NONE]<br />
action1<br />
action2<br />
<br />
Anywhere that NONE appears means that that field is optional.<br />
Warmup: for hovering, this is how long you need to hover over the zone to start the command. For click, this is the delay before the command starts.<br />
Repeat Delay: with how much frequency will the command repeat in the case of a trigger zone.

### Possible Actions (***spaces are critical where they are indicated***)
* Keypresses: simply write the action without quotations (https://talon.wiki/key_action/)
* Swap Zones: swap: NAME_OF_INTERACTION_ZONE_FILE
* Rebinding: for example rebinding a->b and unbinding a.
	* bind: a,b
	* unbind: a
* Text Insertion: simply write the text that you want to insert

### Configuration Examples
A<br />
on click<br />
a<br />
<br />This will simply press the 'a' key when the zone is clicked.

A SPAM<br />
on click trigger 0 0.5<br />
a<br />
a:up<br />
<br />When you click this interaction zone the first time it will output the key 'a' immediately every 0.5s. When you click this interaction zone again, it will immediately fire 'a:up' so as to stop pressing 'a'.
<br />
<br />ENTER<br />
on hover trigger 1<br />
shift:down<br />
shift:up<br />
<br />When you hover over the interaction zone for 1s, it will trigger the key 'shift:down' once. When you hover over the zone again for 1s, it will stop the 'shift' by firing 'shift:up'.


### Note:
* (Advanced users) all generated files are placed in ...user/GanzInteractionZones/ feel free to manually export pngs directly to this folder as well as manually adjust the generated configuration files.
