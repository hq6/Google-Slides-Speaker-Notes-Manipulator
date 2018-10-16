#!/usr/bin/python

# Compatibility with Python3
from __future__ import print_function

# Parsing options
from docopt import docopt

from sys import exit, argv

# Nested dictionaries
from collections import defaultdict

# Find slide boundaries
import re

# Common functions
from common_utils import getService, getAllText

# Read speaker notes from a file delimited by 80 instances of '=' followed by
# Slide # on another line.
def parseNotes(notesFile):
    if not notesFile:
        return {}
    result = {}
    currentLines = []
    possibleNewSlide = False
    previousSlideNum = None
    with open(notesFile) as notes:
      for line in notes:
        line = line.rstrip()
        currentLines.append(line)
        if line.startswith("=" * 80):
          possibleNewSlide = True
          continue
        if possibleNewSlide:
          # See if a new slide matches
          match = re.match(r"Slide ([1-9]\d*)", line)
          if match:
            slideNum = int(match.group(1))
            if previousSlideNum:
              result[previousSlideNum] = "\n".join(currentLines[:-2])
            previousSlideNum = slideNum
            currentLines = []

          possibleNewSlide = False
    # The last slide should be added
    if previousSlideNum:
        result[previousSlideNum] = "\n".join(currentLines)
    return result

doc = r"""
Usage: ./InsertNotes.py [-c] <presentation_id> [<notes>]

    -h,--help           show this
    -c,--clear          When set, clear all the notes in the presentation.
    <presentation_id>   the presentation to update
    <notes>             A text file with records beginning with 80 '=' characters, and Slide N.
"""
def main():
    options = docopt(doc)
    print(options)

    # Parse the notes
    notes = parseNotes(options['<notes>'])

    # Test what was read
    if notes:
      for x in range(1, max(notes.keys()) + 1):
        if x not in  notes: continue
        print("=" * 80)
        print("Slide {0}".format(x))
        print(notes[x])

    # Clear argv so that the oauth service does not freak out
    del argv[1:]
    service = getService()

    # Call the Slides API
    try:
        print("Processing presentation {0}".format(options['<presentation_id>']))
        presentation = service.presentations().get(
            presentationId=options['<presentation_id>']).execute()
        slides = presentation.get('slides')
    except:
        print("Failed to get slides, likely invalid presentation id passed")
        exit(1)


    print('The presentation contains {} slides.'.format(len(slides)))

    # Build the requests -- build a set of requests to automatically
    # upload a set of notes to google slides
    def recursive_defaultdict():
        return defaultdict(recursive_defaultdict)
    def createDeleteRequest(notesId):
	request = recursive_defaultdict()
	request["deleteText"]["objectId"] = notesId
	request["deleteText"]["textRange"]['type'] = 'ALL'
        return request

    # pageElements are the elements of the notes page.
    def notesExist(notesId, pageElements):
        for element in pageElements:
          if element['objectId'] == notesId:
              return getAllText(element)
        return False

    requests = []

    # Extract notes.
    for i, slide in enumerate(slides):
	slideNum = i + 1
        # Find all elements matching the criteria
        # print("Slide {0}".format(slideNum))
        notesPage = slide["slideProperties"]["notesPage"]
        notesId = notesPage["notesProperties"]["speakerNotesObjectId"]
        # We have to check if the notes exist because Google Slides API is
        # silly and doesn't just treat deletions of non-existent elements as
        # no-ops
        if options['--clear'] and notesExist(notesId, notesPage['pageElements']):
            requests.append(createDeleteRequest(notesId))
            continue

	if slideNum not in notes:
	  continue
	# Delete all text
        if notesExist(notesId, notesPage['pageElements']):
	    requests.append(createDeleteRequest(notesId))

	# Insert new text
	request = recursive_defaultdict()
	request["insertText"]["objectId"] = notesId
	request["insertText"]["insertionIndex"] = 0
	request["insertText"]["text"] = notes[slideNum]
	requests.append(request)

    # Send the requests
    if len(requests) == 0:
        print("No notes found")
        return
    body = { 'requests': requests }
    response = service.presentations().batchUpdate(
                presentationId=options['<presentation_id>'], body=body).execute()

if __name__ == '__main__':
    main()
