build:
	docker-compose build

run-example:
	docker-compose run --rm unicorm python examples/$(example).py

tests:
	docker-compose run --rm unicorm py.test -vv -p no:cacheprovider test
