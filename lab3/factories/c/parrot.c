#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

typedef struct Parrot {
    PTRFUN* vtable;
    char const* name;
} Parrot;

char const* name(void* this) {
    return ((Parrot*)this)->name;
}

char const* parrot_greet(void) {
    return "Squawk";
}

char const* parrot_menu(void) {
    return "Seeds";
}

PTRFUN parrot_vtable[3] = {name, parrot_greet, parrot_menu};

size_t size(){
  return sizeof(Parrot);
}

void construct(Parrot* parrot, const char* name) {
    parrot->name = name;
    parrot->vtable = parrot_vtable;
}

void* create(const char* name) {
    Parrot* parrot = malloc(sizeof(Parrot));
    construct(parrot, name);

    return parrot;
}