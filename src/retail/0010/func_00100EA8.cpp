struct Callback { unsigned char pad[0x18]; short adjust; unsigned char pad2[2]; void (*call)(void*); };
struct Object { unsigned char pad[0x24]; void* active; unsigned char pad2[0x10]; Callback* callback; };
struct Entry { Object* object; unsigned int enabled; };
extern "C" Entry D_597BD0[128] __attribute__((section(".data")));
extern "C" void func_00100EA8() {
    for (unsigned int i = 0; i < 0x80; ++i) {
        Entry* entry = &D_597BD0[i];
        if (entry->enabled != 0) {
            Object* object = entry->object;
            if (object->active != 0) {
                Callback* callback = object->callback;
                callback->call((char*)object + callback->adjust);
            }
        }
    }
}