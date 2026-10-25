struct CallbackTable {
    unsigned char padding[0x10];
    short offset;
    unsigned char alignment[2];
    float (*callback)(void*);
};

struct Object {
    CallbackTable* callbacks;
};

extern "C" int func_00111338(Object*);

extern "C" float func_001112F0(Object* object) {
    if (func_00111338(object)) {
        return 0.0f;
    }
    CallbackTable* callbacks = object->callbacks;
    return callbacks->callback(reinterpret_cast<unsigned char*>(object) + callbacks->offset);
}
