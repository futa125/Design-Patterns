#include <cstdint>
#include <iostream>
using namespace std;

class B {
   public:
    virtual int prva() = 0;
    virtual int druga(int) = 0;
};

class D : public B {
   public:
    virtual int prva() {
        return 42;
    }
    virtual int druga(int x) {
        return prva() + x;
    }
};

typedef int (*PFUN1)(B*);
typedef int (*PFUN2)(B*, int);

void printReturnValues(B* pb) {
    uintptr_t vtable_address = *(uintptr_t*)pb;

    PFUN1 fn1 = *reinterpret_cast<PFUN1*>(vtable_address)[0];
    PFUN2 fn2 = *reinterpret_cast<PFUN2*>(vtable_address)[1];

    cout << fn1(pb) << endl;
    cout << fn2(pb, 5) << endl;
}

int main(void) {
    D* pb = new D();
    printReturnValues(pb);
}
