# Raylib Kod Ornekleri - Makefile
# Kullanim: make all   (tum ornekleri derle)
#           make ornek01  (tek ornegi derle)
#           make clean  (temizle)
#
# Onkoşul: raylib kurulu olmali
#   macOS:  brew install raylib
#   Linux:  sudo apt install libraylib-dev

CC = cc
CFLAGS = -Wall -std=c99
LDFLAGS = -lraylib -lm

# macOS icin ek baglantilar
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -framework IOKit -framework Cocoa -framework OpenGL
endif
ifeq ($(UNAME_S),Linux)
    LDFLAGS += -lGL -lpthread -ldl -lrt -lX11
endif

SOURCES = $(wildcard *.c)
TARGETS = $(SOURCES:.c=)

all: $(TARGETS)

ornek01: ornek01_temel_pencere.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

ornek02: ornek02_kure_cizimi.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

ornek03: ornek03_viewport_ve_isinlar.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

ornek04: ornek04_basit_raytracer.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

ornek05: ornek05_diffuse_aydinlatma.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

ornek06: ornek06_specular_aydinlatma.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f ornek01 ornek02 ornek03 ornek04 ornek05 ornek06

.PHONY: all clean
