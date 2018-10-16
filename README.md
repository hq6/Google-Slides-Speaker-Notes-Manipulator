# Google Slides Notes Manipulation Utility

[Google Slides](slides.google.com) is a great tool for collaborating on
presentations, but its feature set is somewhat limited. This tool uses the API
to work around a specific limitation: the inability to export and import the
speaker notes associated with each slide.

Without this tool, if one wanted to print out just the speaker notes associated
with a presentation, one would have to manually copy and paste the notes from
each slide using the Slides UI. Furthermore, if one wanted to edit the notes in
one's favorite text editor, it would be necessary to manually copy and paste
the notes back into Google Slides.

# Usage

Extract speaker notes from a presentation.

    ./ExtractNotes.py <presentation_id>  >Notes.txt

Insert speaker notes into a presentation.

    ./InsertNotes.py <presentation_id> Notes.txt

When editing notes, it suffices to maintain the format of the following delimiter for each slide.

```
================================================================================
Slide #
```

# Dependencies

 * [Google API Python Client](https://developers.google.com/slides/how-tos/libraries#python).

```
 pip install --upgrade google-api-python-client
```
 * OAuth 2 Client
```
sudo pip install --upgrade oauth2client
```

 * Docopt
```
 pip install docopt
```

# One-Time Setup

Given that this app is deployed as a stand-alone script rather than hosted on a web server, the author cannot provide client keys and secrets. Therefore, users must visit the [Google Slides API page](https://developers.google.com/slides/quickstart/python) and perform the following steps for initial setup.

1. Click on "Enable The Google Slides API"
2. Create a project.
3. Click "Next"
4. Click "Download Client Configuration" and save credentials.json in the
   directory this application will be executed from.
