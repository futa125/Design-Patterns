#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

typedef struct Tiger {
    PTRFUN* vtable;
    char const* name;
} Tiger;

char const* name(void* this) {
    return ((Tiger*)this)->name;
}

char const* tiger_greet(void) {
    return "Rawr";
}

char const* tiger_menu(void) {
    return "Antelopes";
}

PTRFUN tiger_vtable[3] = {name, tiger_greet, tiger_menu};

size_t size(){
  return sizeof(Tiger);
}

void construct(Tiger* tiger, const char* name) {
    tiger->name = name;
    tiger->vtable = tiger_vtable;
}

void* create(const char* name) {
    Tiger* tiger = malloc(sizeof(Tiger));
    construct(tiger, name);

    return tiger;
}
