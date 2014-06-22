# makefile
# Use 'make makefile' to install to the current user's inkscape extensions folder.
# Files:
# hideframelayers.inx hideframelayers.py importpenciltest.inx importpenciltest.py outputframes.inx outputframes.py README


DESTINATION=~/.config/inkscape/extensions/

all: 
	cp *.inx $(DESTINATION)
	cp *.py $(DESTINATION)
	cp README $(DESTINATION)

