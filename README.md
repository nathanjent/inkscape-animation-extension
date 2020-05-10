# Inkscape Animation Extension

---
This extension can import a series of image files and place them into frame
numbered layers. Each frame layer consists of sub-layers for inking over the
images. An output extension is included. It saves a series of images using the
inked frame layers. ffmpeg or a similar program can then be used to make as
movie file from these images.

[Download version 0.4](http://nathanjent.com/downloads/inkscape-animation-extension_0.4.zip)

A simple example that I created in about a minute:

![Sample Animation of Bouncing Ball](./animationextensionexample.svg)

(example can only be viewed in a browser which supports svg like Firefox or Chrome)

## USAGE

Begin by using the 'Import/Create Frames' extension. I recommend starting with a
new inkscape document when importing your pencil frames. But the new frames will
not affect any existing layers. I like to create my pencil test using
[Pencil](http://www.pencil-animation.org/)

1. Input the frame range you'd like to import/create.
2. Input the frame duration. This is used to preview the animation by loading
the svg file in a supported browser like Firefox. The timing works best when
animations start from frame 1. Keeping the amount of frames low helps inkscape
run better.
3. It is recommended to set the document dimensions equal to the imported image
size.
4. Set the import options: Check the box to import images. The base filename
should include the directory but not the frame number or file type extension. If
you save your inkscape file in the same directory as your imported images you
can get away with just using the filename. Then enter the filetype extension of
your imported images. The imported files must be named with a trailing 3 digit
frame number before the file extension. Frame numbers should be between 001
and 999. If the pencil images have more than a 3 digit frame number be sure to apend
the first digits to the file name. (example: /home/inkscaper/frame00001.png
would become /home/inkscaper/frame00 in the extension dialog)
5. Background color can be set on the background tab. If you only need a static
background, hide all of the background layers and create a new layer under all
of the frame layers.
6. Apply the extension to create a series of numbered layers with four
sub-layers: ink, paint, pencil, and background. The pencil layer will contain
the imported images. The background layer will contain a colored rectangle
filling in the document boundary.

The 'Set Frame Options' extension is used to adjust the frame duration, display
the frame numbers, and to hide or lock multiple layers/sublayers.  Frame
duration settings work best when setting the 'From' frame to 1 and the 'To'
frame to the last frame layer number.

Once you have all of your frames inked and painted its time to run the output
extension. Enter the directory and the base filename without the extension and
apply. This should give you a series of inked image frames to input into ffmpeg
or maybe imagemagick and create a movie or gif file. The extension only outputs
to png format. This is a limitation set by the Inkscape exporter.

## TODO

- [ ] Update extension for Inkscape 1.0
- [ ] Fix bug with option to hide pencil layers during output.
- [ ] Add option to choose background image(s).
- [ ] Add option to choose sub-layer names.

## LICENSE

GPL2

## Installation

Copy the .inx and .py files into ~/.config/inkscape/extensions/ and restart
inkscape. Or use the makefile to install.

For global installation place in /usr/share/inkscape/extensions
(your distro may vary)

For Windows place in \Inkscape\share\extensions\
