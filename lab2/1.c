#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int gt_int(const void* left, const void* right) {
    return *(int*)left > *(int*)right;
}

int gt_char(const void* left, const void* right) {
    return *(char*)left > *(char*)right;
}

int gt_str(const void* left, const void* right) {
    return strcmp(*(char**)left, *(char**)right) > 0;
}

const void* mymax(const void* base, const size_t nmemb, const size_t size, int (*compar)(const void*, const void*)) {
    const void* max = &base[size];
    const void* curr;

    for (int i = 1; i < nmemb; i++) {
        curr = &base[i * size];
        if (compar(curr, max)) {
            max = curr;
        }
    }

    return max;
}

int main() {
    const int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    const char arr_char[] = "Suncana strana ulice";
    const char* arr_str[] = {
        "Gle",
        "malu",
        "vocku",
        "poslije",
        "kise",
        "Puna",
        "je",
        "kapi",
        "pa",
        "ih",
        "njise",
    };

    const int* max_int = (const int*)mymax(arr_int, sizeof(arr_int) / sizeof(*arr_int), sizeof(int), gt_int);
    const char* max_char = (const char*)mymax(arr_char, sizeof(arr_char) / sizeof(*arr_char), sizeof(char), gt_char);
    const char** max_str = (const char**)mymax(arr_str, sizeof(arr_str) / sizeof(*arr_str), sizeof(char*), gt_str);

    printf("Max of arr_int: %d\n", *max_int);
    printf("Max of arr_char: %c\n", *max_char);
    printf("Max of arr_str: %s\n", *max_str);
}
