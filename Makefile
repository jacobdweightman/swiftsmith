.PHONY: all
all:
	python3 scripts/run_tests_parallel.py

.PHONY: serial
serial:
	python3 scripts/run_tests.py

.PHONY: test
test:
	sh scripts/generate_test.sh
	./generated/test

.PHONY: clean
clean:
	rm -rf generated/*
