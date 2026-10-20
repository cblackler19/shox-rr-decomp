extern "C" unsigned char D_00446518[];
extern "C" unsigned char D_00446560[];
extern "C" void func_001028F0(void*);
extern "C" void func_00239AC0(void*);

struct Tail {
    unsigned int first;
    unsigned int second;
    unsigned int third;
    void* table;
};

struct Object {
    unsigned char padding0[0x10];
    unsigned int field10;
    unsigned char padding1[0x248 - 0x14];
    Tail tail;
    void* descriptor;
};

extern "C" Object* func_00102628(Object* object) {
    object->descriptor = D_00446518;
    func_001028F0(object);
    object->field10 = 0;
    func_00239AC0(reinterpret_cast<unsigned char*>(object) + 0x18);
    Tail* tail = &object->tail;
    tail->table = D_00446560;
    tail->first = 0;
    tail->second = 0;
    tail->third = 0;
    return object;
}
