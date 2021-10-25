#!/usr/bin/env python3
from zipfile import ZipFile
import shutil
import sys
import os

if len(sys.argv) < 4:
    print("Usage: {} <script file> <original document> <new document>".format(sys.argv[0]))
    exit()

MACRO_FILE = sys.argv[1]
ORIGINAL_DOCUMENT_FILE= sys.argv[2]
NEW_DOCUMENT_FILE = sys.argv[3]
MANIFEST_PATH = 'META-INF/manifest.xml';
EMBED_PATH = 'Scripts/python/' + MACRO_FILE;

hasMeta = False
with ZipFile(ORIGINAL_DOCUMENT_FILE) as bundle:
    # grab the manifest
    manifest = []
    for rawLine in bundle.open('META-INF/manifest.xml'):
        line = rawLine.decode('utf-8');
        if MACRO_FILE in line:
            hasMeta = True
        if ('</manifest:manifest>' in line) and (hasMeta == False):
            for path in ['Scripts/','Scripts/python/', EMBED_PATH]:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{}"/>\n'.format(path))
        manifest.append(line)

    # remove the manifest and script file
    with ZipFile(NEW_DOCUMENT_FILE, 'w') as tmp:
        for item in bundle.infolist():
            buffer = bundle.read(item.filename)
            if (item.filename not in [MANIFEST_PATH, EMBED_PATH]):
                tmp.writestr(item, buffer)

with ZipFile(NEW_DOCUMENT_FILE, 'a') as bundle:
    bundle.write(MACRO_FILE, EMBED_PATH)
    bundle.writestr(MANIFEST_PATH, ''.join(manifest))

print("Added {} to {}".format(MACRO_FILE, NEW_DOCUMENT_FILE))
