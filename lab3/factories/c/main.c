#include <stdio.h>
#include <stdlib.h>

#include "myfactory.h"

typedef char const* (*PTRFUN)();

typedef char const* (*NAMEFUN)(void*);
typedef char const* (*GREETFUN)();
typedef char const* (*MENUFUN)();

typedef struct Animal {
    PTRFUN* vtable;
    // vtable entries:
    // 0: char const* name(void* this);
    // 1: char const* greet();
    // 2: char const* menu();
} Animal;

void print_greeting(Animal* animal) {
    NAMEFUN name = (NAMEFUN)(animal->vtable[0]);
    GREETFUN greet = (GREETFUN)(animal->vtable[1]);

    printf("%s says %s!\n", name(animal), greet());
}

void print_menu(Animal* animal) {
    NAMEFUN name = (NAMEFUN)(animal->vtable[0]);
    MENUFUN menu = (MENUFUN)(animal->vtable[2]);

    printf("%s likes to eat %s!\n", name(animal), menu());
}

int main(int argc, char* argv[]) {
    for (int i = 0; i < argc / 2; ++i) {
        const char* libname = argv[1 + 2 * i];
        const char* animal_name = argv[1 + 2 * i + 1];

        printf("HEAP:\n");
        Animal* animal_heap = (Animal*)myfactory_heap(libname, animal_name);
        if (!animal_heap) {
            printf("Creation of plug-in object %s failed.\n\n", libname);
            continue;
        }

        print_greeting(animal_heap);
        print_menu(animal_heap);
        free(animal_heap);
        printf("\n");

        printf("STACK:\n");
        Animal* animal_stack = alloca(size(libname));
        if (myfactory_stack(libname, animal_name, animal_stack) == -1) {
            printf("Creation of plug-in object %s failed.\n\n", libname);
            continue;
        }

        print_greeting(animal_stack);
        print_menu(animal_stack);
        // free(animal_stack);
        printf("\n");
    }
}