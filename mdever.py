#!/usr/bin/env python3
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import markdown2
import sys
import mimetypes
def convertENML(md):
    enml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    enml += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n\n'
    enml += '<en-note>\n'
    enml += markdown2.markdown(md)
    enml += '</en-note>\n'
    return enml


def argv_check():
    if len(sys.argv) != 2:
        print("""ERROR: File name missing
Usage:
    mdever example.md""")
        quit()


def file_check():
    mime = mimetypes.guess_type(sys.argv[1])
    if mime[0] != "text/markdown":
        print("ERROR: {input_filename} is wrong file ({mime})".format(
            input_filename=sys.argv[1], mime=mime[0]))
        quit()


def mdever():
    # Open markdown file
    mdfile = sys.argv[1]
    while True:
        try:
            f = open(mdfile, "r")
            break
        except:
            print("ERROR: Can't open file: {filename}".format(filename=mdfile))
            quit()
    markdown_content = f.read()
    f.close()

    # Trans markdown -> enml
    enml = convertENML(markdown_content)
    # Connect Evernote
    dev_token = "S=s1:U=93787:E=162439a6ac8:C=15aebe93e40:P=1cd:A=en-devtoken:V=2:H=227be9400f1886b4fa570e0cb012fcab"
    client = EvernoteClient(token=dev_token)
    noteStore = client.get_note_store()

    # Create new note
    note = Types.Note()
    note.title = "1st test note"
    note.content = enml
    note = noteStore.createNote(note)


if __name__ == "__main__":
    argv_check()
    file_check()
    mdever()
