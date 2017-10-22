build:
	docker-compose build

tests:
	docker-compose run --rm sqlchemistry py.test -vv -p no:cacheprovider test
