CC := g++
CFLAGS := -fPIC -c -O3 -g -Wall
CFLAGS += -I../include -L../lib -DLCOMP_LINUX=1

NAME := wlcomp

lib: lib$(NAME).so

lib$(NAME).so: $(NAME).o
	$(CC) -shared -Wl,-soname,lib$(NAME).so -o lib$(NAME).so $(NAME).o -lc

$(NAME).o: wlcomp.cpp
	$(CC) $(CFLAGS) wlcomp.cpp

clean:
	rm *.o *.so
