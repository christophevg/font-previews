all: fonts

fonts:
	mkdir -p $@
	python gen.py $@ > $@/index.json

.PHONY: fonts

prune:
	python prune.py fonts > fonts/index.pruned.json
	rm fonts/index.json
	mv fonts/index.pruned.json fonts/index.json

clean:
	rm -rf fonts
