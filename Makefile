REP = util/replace

all: dist/merching.py

dist/merching.py: tmp/merching.html dist
	$(REP) tmp/merching.html src/merching.py HTML -o dist/merching.py
	chmod +x dist/merching.py

tmp/merching.html: src/merching.css src/merching.js tmp
	$(REP) src/merching.css src/merching.html CSS -o tmp/merching.tmp
	$(REP) src/merching.js tmp/merching.tmp JS -o tmp/merching.html
	rm tmp/merching.tmp

tmp:
	mkdir -p tmp

dist:
	mkdir -p dist

clean:
	rm -rf tmp dist
