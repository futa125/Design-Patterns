#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

struct Animal {
    struct AnimalFunctions* vtable;
    char const* name;
};

struct ProducingAnimal {
    struct ProducingAnimalFunctions* vtable;
    char const* name;
    char const* species;
};

struct AnimalFunctions {
    PTRFUN greet;
    PTRFUN menu;
};

struct ProducingAnimalFunctions {
    PTRFUN greet;
    PTRFUN menu;
    PTRFUN produce;
};

const char* dogGreet() {
    return "vau!";
}

const char* dogMenu() {
    return "kuhanu govedinu";
}

const char* catGreet() {
    return "mijau!";
}

const char* catMenu() {
    return "konzerviranu tunjevinu";
}

const char* cowGreet() {
    return "moo!";
}

const char* cowMenu() {
    return "trava";
}

const char* cowProduces() {
    return "milk";
}

struct AnimalFunctions dogFunctions = {
    &dogGreet,
    &dogMenu,
};

struct AnimalFunctions catFunctions = {
    &catGreet,
    &catMenu,
};

struct ProducingAnimalFunctions cowFunctions = {
    &cowGreet,
    &cowMenu,
    &cowProduces,
};

void constructDog(struct Animal* dog, const char* name) {
    dog->name = name;
    dog->vtable = &dogFunctions;
}

void constructCat(struct Animal* cat, const char* name) {
    cat->name = name;
    cat->vtable = &catFunctions;
}

void constructCow(struct ProducingAnimal* cow, const char* name, const char* species) {
    cow->name = name;
    cow->species = species;
    cow->vtable = &cowFunctions;
}

struct Animal* createDog(const char* name) {
    struct Animal* dog = malloc(sizeof(struct Animal));

    constructDog(dog, name);

    return dog;
}

struct Animal* createCat(char const* name) {
    struct Animal* cat = malloc(sizeof(struct Animal));

    constructCat(cat, name);

    return cat;
}

struct ProducingAnimal* createCow(char const* name, char const* species) {
    struct ProducingAnimal* cow = malloc(sizeof(struct ProducingAnimal));

    constructCow(cow, name, species);

    return cow;
}

void animalPrintGreeting(const struct Animal* animal) {
    printf("%s pozdravlja: %s\n", animal->name, animal->vtable->greet());
}

void animalPrintMenu(const struct Animal* animal) {
    printf("%s voli %s\n", animal->name, animal->vtable->menu());
}

void testAnimals() {
    struct Animal* p1 = createDog("Hamlet");
    struct Animal* p2 = createCat("Ofelija");
    struct Animal* p3 = createDog("Polonije");
    struct ProducingAnimal* p4 = createCow("milka", "krava");

    animalPrintGreeting(p1);
    animalPrintGreeting(p2);
    animalPrintGreeting(p3);
    animalPrintGreeting((struct Animal*)p4);

    animalPrintMenu(p1);
    animalPrintMenu(p2);
    animalPrintMenu(p3);

    free(p1);
    free(p2);
    free(p3);
}

struct Animal* createNDogs(int n) {
    struct Animal* dogs = malloc(n * sizeof(struct Animal));
    char* name;

    for (int i = 0; i < n; i++) {
        asprintf(&name, "Dog %d", i + 1);
        dogs[i] = *(createDog(name));
    }

    return dogs;
}

int main() {
    testAnimals();
    printf("\n");

    int n = 3;
    struct Animal* dogs = createNDogs(n);
    for (int i = 0; i < n; i++) {
        animalPrintGreeting(&dogs[i]);
        animalPrintMenu(&dogs[i]);
    }
    free(dogs);
    printf("\n");

    struct Animal p1;
    p1.name = "Hamlet";
    p1.vtable = &dogFunctions;

    struct Animal p2;
    p2.name = "Ofelija";
    p2.vtable = &catFunctions;

    struct Animal p3;
    p3.name = "Polonije";
    p3.vtable = &dogFunctions;

    animalPrintGreeting(&p1);
    animalPrintGreeting(&p2);
    animalPrintGreeting(&p3);

    animalPrintMenu(&p1);
    animalPrintMenu(&p2);
    animalPrintMenu(&p3);
}
