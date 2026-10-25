extern "C" void func_00286D10(int);

struct Object_00112320 {
    char pad0[52];
    unsigned int value52;
    char pad56[24];
    int count80;
    char pad84[36];
    int value120;
};

extern "C" void func_00112320(Object_00112320 *self) {
    if (self->count80) {
        func_00286D10(self->count80 - 1);
    }
    self->value120 = 0;
    self->value52 = ~0u;
}
