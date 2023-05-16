#include "myfactory.h"

#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef size_t (*SIZEFUN)();
typedef void (*CONSTRUCTFUN)(void*, char const*);
typedef void* (*CREATEFUN)(char const*);

size_t size(char const* libname) {
    char filename[strlen(libname) + strlen(".so") + 1];
    sprintf(filename, "%s%s", libname, ".so");

    void* handle = dlopen(filename, RTLD_LAZY);
    if (handle == NULL) {
        fprintf(stderr, "%s\n", dlerror());
        return 0;
    }

    SIZEFUN size = (SIZEFUN)dlsym(handle, "size");
    if (size == NULL) {
        fprintf(stderr, "%s\n", dlerror());
        return 0;
    }

    return size();
}

void* myfactory_heap(char const* libname, char const* ctorarg) {
    char filename[strlen(libname) + strlen(".so") + 1];
    sprintf(filename, "%s%s", libname, ".so");

    void* handle = dlopen(filename, RTLD_LAZY);
    if (handle == NULL) {
        fprintf(stderr, "%s\n", dlerror());
        return NULL;
    }

    CREATEFUN create = (CREATEFUN)dlsym(handle, "create");
    if (create == NULL) {
        fprintf(stderr, "%s\n", dlerror());
        return NULL;
    }

    return create(ctorarg);
}

int myfactory_stack(char const* libname, char const* ctorarg, void* obj) {
    char filename[strlen(libname) + strlen(".so") + 1];
    sprintf(filename, "%s%s", libname, ".so");

    void* handle = dlopen(filename, RTLD_LAZY);
    if (handle == NULL) {
        fprintf(stderr, "%s\n", dlerror());
        return -1;
    }

    CONSTRUCTFUN construct = (CONSTRUCTFUN)dlsym(handle, "construct");
    if (construct == NULL) {
        fprintf(stderr, "%s\n", dlerror());
        return -1;
    }

    construct(obj, ctorarg);

    return 0;
}