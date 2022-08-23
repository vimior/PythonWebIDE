
CC=gcc
CFLAGS=-c -Wall -g

OBJS=main.o utils.o

main:$(OBJS)
    $(CC $^ -o main

%.o:%.cpp
    $(CC) $^ $(CFLAGS) -o $@
clean:
    rm *.o main