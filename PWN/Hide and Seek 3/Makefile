all: dist/dist.zip dist/chall

dist/chall: src/chall.c
	gcc -o dist/chall src/chall.c -w -z relro -z now -fstack-protector-all

dist/dist.zip: src/run.sh dist/chall Dockerfile docker-compose.yml
	zip dist/dist.zip dist/chall src/run.sh Dockerfile docker-compose.yml
