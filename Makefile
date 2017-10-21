build:
	docker-compose build

tests: build
	docker-compose run --rm sqlchemistry py.test -vv -p no:cacheprovider test
