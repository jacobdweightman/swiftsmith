.PHONY: all
all:
	python3 scripts/run_tests.py $(START_SEED)

.PHONY: test
test:
	sh scripts/generate_test.sh
	./generated/test

.PHONY: clean
clean:
	rm -rf generated/*
