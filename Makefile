runimg:
		@docker run --rm --name reimburse -it -p 8080:8080 -v $$(pwd):/app/ --env-file dot-env-template reimburse
buildimg:
		@docker build -t reimburse .
