struct Context {
    unsigned char padding0[0x48];
    short offset;
    unsigned char padding1[2];
    int (*callback)(void*);
};

struct Object {
    unsigned char padding0[0x14];
    Context* context;
    unsigned char padding1[0x68 - 0x18];
    int key;
};

struct Input { int key; };

extern "C" void func_0010A9C8(Object* object, const Input* input) {
    if (input->key == object->key) {
        Context* context = object->context;
        short offset = context->offset;
        int (*callback)(void*) = context->callback;
        callback(reinterpret_cast<unsigned char*>(object) + offset);
    }
}
