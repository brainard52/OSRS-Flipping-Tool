REP = util/replace

.PHONY: all
all: dist/merching.py

dist/merching.py: tmp/merching.html
	mkdir -p tmp dist
	$(REP) tmp/merching.html src/merching.py HTML -o tmp/merching.tmp
	sed 's/ -c "exit()"//' tmp/merching.tmp > dist/merching.py
	rm tmp/merching.tmp
	chmod +x dist/merching.py

tmp/merching.html: src/merching.css src/merching.js
	mkdir -p tmp
	$(REP) src/merching.css src/merching.html CSS -o tmp/merching.tmp
	$(REP) src/merching.js tmp/merching.tmp JS -o tmp/merching.html
	rm tmp/merching.tmp

.PHONY: lint
lint: all
	pylint dist/merching.py

.PHONY: clean
clean:
	rm -rf tmp dist
