#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef double (*PTRFUN)();

/*
    UnaryFunction
*/

struct UnaryFunction {
    struct UnaryFunctionTable* vtable;
    int lower_bound;
    int upper_bound;
};

struct UnaryFunctionTable {
    PTRFUN value_at;
    PTRFUN negative_value_at;
};

double negative_value_at(struct UnaryFunction* fn, double x) {
    return -1 * fn->vtable->value_at(fn, x);
}

void tabulate(struct UnaryFunction* fn) {
    for (int x = fn->lower_bound; x <= fn->upper_bound; x++) {
        printf("f(%d)=%lf\n", x, fn->vtable->value_at(fn, (double)x));
    }
}

bool same_functions_for_ints(struct UnaryFunction* f1, struct UnaryFunction* f2, double tolerance) {
    if (f1->lower_bound != f2->lower_bound) {
        return false;
    }

    if (f1->upper_bound != f2->upper_bound) {
        return false;
    }

    for (int x = f1->lower_bound; x <= f1->upper_bound; x++) {
        double delta = f1->vtable->value_at(f1, (double)x) - f2->vtable->value_at(f2, (double)x);
        if (delta < 0) {
            delta = -delta;
        }

        if (delta > tolerance) {
            return false;
        }
    }

    return true;
}

struct UnaryFunctionTable unaryFunctionTable = {
    NULL,  // Not implemented
    &negative_value_at,
};

void constructUnaryFunction(struct UnaryFunction* fn, int lower_bound, int upper_bound) {
    fn->lower_bound = lower_bound;
    fn->upper_bound = upper_bound;
    fn->vtable = &unaryFunctionTable;
}

struct UnaryFunction* createUnaryFunction(int lower_bound, int upper_bound) {
    struct UnaryFunction* fn = malloc(sizeof(struct UnaryFunction));

    constructUnaryFunction(fn, lower_bound, upper_bound);

    return fn;
}

/*
    Square
*/

struct Square {
    struct UnaryFunctionTable* vtable;
    int lower_bound;
    int upper_bound;
};

double square_value_at(struct Square* square, double x) {
    return x * x;
}

struct UnaryFunctionTable squareFunctionTable = {
    &square_value_at,
    &negative_value_at,
};

struct Square* createSquare(int lower_bound, int upper_bound) {
    struct Square* square = malloc(sizeof(struct Square));

    constructUnaryFunction((struct UnaryFunction*)square, lower_bound, upper_bound);
    square->vtable = &squareFunctionTable;

    return square;
}

/*
    Linear
*/

struct Linear {
    struct UnaryFunctionTable* vtable;
    int lower_bound;
    int upper_bound;
    double a;
    double b;
};

double linear_value_at(struct Linear* linear, double x) {
    return linear->a * x + linear->b;
}

struct UnaryFunctionTable linearFunctionTable = {
    &linear_value_at,
    &negative_value_at,
};

struct Linear* createLinear(int lower_bound, int upper_bound, double a, double b) {
    struct Linear* linear = malloc(sizeof(struct Linear));

    constructUnaryFunction((struct UnaryFunction*)linear, lower_bound, upper_bound);
    linear->a = a;
    linear->b = b;
    linear->vtable = &linearFunctionTable;

    return linear;
}

int main(void) {
    struct Square* f1 = createSquare(-2, 2);
    tabulate((struct UnaryFunction*)f1);

    struct Linear* f2 = createLinear(-2, 2, 5, -2);
    tabulate((struct UnaryFunction*)f2);

    printf("f1==f2: %s\n", same_functions_for_ints((struct UnaryFunction*)f1, (struct UnaryFunction*)f2, 1E-6) == 1 ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", f2->vtable->negative_value_at(f2, 1.0));

    free(f1);
    free(f2);
}
