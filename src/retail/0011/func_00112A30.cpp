extern "C" char D_00449188[];
extern "C" void func_0010DCE8(void *);

struct Object_00112A30 {
    int field0;
    int field4;
    int field8;
    int field12;
    char pad16[4];
    void *vtable;
    int field24;
    char rest[4];
};

extern "C" Object_00112A30 *func_00112A30(Object_00112A30 *self) {
    self->field0 = 0;
    self->field4 = 0;
    self->field8 = 0;
    self->field12 = 0;
    self->field24 = 0;
    self->vtable = D_00449188;
    func_0010DCE8((char *)self + 28);
    return self;
}
