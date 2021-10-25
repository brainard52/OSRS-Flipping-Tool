from zipfile import ZipFile
import shutil
import sys
import os

if len(sys.argv) < 3:
    print("Usage: {} scriptfile hostdocument".format(sys.argv[0]))
    exit()

MACRO_FILE = sys.argv[1]
DOCUMENT_FILE = sys.argv[2]
MANIFEST_PATH = 'META-INF/manifest.xml';
EMBED_PATH = 'Scripts/python/' + MACRO_FILE;

hasMeta = False
with ZipFile(DOCUMENT_FILE) as bundle:
    
    # grab the manifest
    manifest = []
    for rawLine in bundle.open('META-INF/manifest.xml'):
        line = rawLine.decode('utf-8');
        if MACRO_FILE in line:
            hasMeta = True
        if ('</manifest:manifest>' in line) and (hasMeta == False):
            for path in ['Scripts/','Scripts/python/', EMBED_PATH]:
                manifest.append('<manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{}"/>'.format(path))
        manifest.append(line)

    # remove the manifest and script file
    with ZipFile(DOCUMENT_FILE + '.tmp', 'w') as tmp:
        for item in bundle.infolist():
            buffer = bundle.read(item.filename)
            if (item.filename not in [MANIFEST_PATH, EMBED_PATH]):
                tmp.writestr(item, buffer)


# os.replace(DOCUMENT_FILE + '.tmp', DOCUMENT_FILE);  python 3.3+
os.remove(DOCUMENT_FILE);
shutil.move(DOCUMENT_FILE + '.tmp', DOCUMENT_FILE)

with ZipFile(DOCUMENT_FILE, 'a') as bundle:
    bundle.write(MACRO_FILE, EMBED_PATH)
    bundle.writestr(MANIFEST_PATH, ''.join(manifest))

print("Added the script {} to {}".format(MACRO_FILE, DOCUMENT_FILE))