#!/usr/bin/python

# Compatibility with Python3
from __future__ import print_function

# Parsing options
from docopt import docopt

from sys import exit, argv

# Nested dictionaries
from collections import defaultdict

# Common functions
from common_utils import getService, getAllText

doc = r"""
Usage: ./ExtractNotes.py <presentation_id>

    -h,--help                    show this
"""
def main():
    options = docopt(doc)

    # Clear argv so that the oauth service does not freak out
    del argv[1:]
    service = getService()

    # Call the Slides API
    try:
        presentation = service.presentations().get(
            presentationId=options['<presentation_id>']).execute()
        slides = presentation.get('slides')
    except:
        print("Failed to get slides, likely invalid presentation id passed")
        exit(1)

    # Extract notes.
    for i, slide in enumerate(slides):
        # Find all elements matching the criteria
        print("=" * 80)
        print("Slide {0}".format(i+1))
        notesPage = slide["slideProperties"]["notesPage"]
        notesId = notesPage["notesProperties"]["speakerNotesObjectId"]
        for element in notesPage['pageElements']:
            if element['objectId'] == notesId:
              print(getAllText(element))

if __name__ == '__main__':
    main()
