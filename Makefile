all: Merching.ods site-packages.zip


Merching.ods: Merching_base.ods
	./embed-py Merching.py Merching_base.ods Merching.ods

site-packages.zip:
	mkdir -p site-packages temp
	pip3 download certifi charset_normalizer idna requests urllib3 -d temp
	find temp -name "*.whl" -type f -exec unzip -d site-packages {} \;
	zip -r site-packages.zip site-packages/

clean:
	rm -rf Merching.ods site-packages.zip site-packages temp

