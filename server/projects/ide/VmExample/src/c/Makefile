
CC=gcc
CFLAGS=-c -Wall -g

OBJS=main.o hello.o

ALL: main

main:$(OBJS)
    $(CC $^ -o main

%.o:%.c
    $(CC) $^ $(CFLAGS) -o $@
clean:
    rm *.o main