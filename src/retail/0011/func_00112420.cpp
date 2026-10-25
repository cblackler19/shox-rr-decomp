extern "C" void *D_0032B550[];
extern "C" unsigned char D_00458E00[];
extern "C" void func_001A1CA0(void *, int, void *);
extern "C" void func_001A4BF0(void *);
extern "C" void func_00286D10(int);
extern "C" void func_002869F0(int);
extern "C" void func_00112508(void *);

struct Subobject_00112420 {
    char pad[20];
    int flags;
};
struct Object_00112420 {
    char pad0[24];
    int field24;
    char pad28[16];
    int flags44;
    char pad48[32];
    int count80;
    char pad84[48];
    int field132;
};

extern "C" void func_00112420(Object_00112420 *self) {
    self->field132 = 0;
    Subobject_00112420 *sub = (Subobject_00112420 *)((char *)self + 24);
    if (sub->flags < 0) {
        int flags = sub->flags;
        func_001A1CA0(D_0032B550[0], (flags << 1) >> 1, sub);
        sub->flags &= 0x7fffffff;
    }
    func_001A4BF0(D_00458E00);
    if (self->count80) {
        func_00286D10(self->count80 - 1);
        func_002869F0(self->count80 - 1);
        self->count80 = 0;
        func_00112508(self);
    }
}
