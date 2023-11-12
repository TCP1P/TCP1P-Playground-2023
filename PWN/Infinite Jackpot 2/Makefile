all:
	gcc -o dist/chall src/chall.c -w -z relro -z now -fstack-protector-all
	zip dist/dist.zip dist/chall src/run.sh Dockerfile docker-compose.yml
