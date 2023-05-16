#include <stdio.h>

typedef enum MemoryLocation {
    Heap,
    Stack,
} MemoryLocation;

size_t size(char const* libname);
void* myfactory_heap(char const* libname, char const* ctorarg);
int myfactory_stack(char const* libname, char const* ctorarg, void* obj);
