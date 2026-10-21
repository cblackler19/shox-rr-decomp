struct func_0010F480_Callback { unsigned char pad0[0x50]; short offset; short pad54; void (*call)(void *); };
struct func_0010F480_Object { unsigned char pad0[0x14]; func_0010F480_Callback *callback; unsigned char pad18[0x68]; int field80; int field84; };

extern "C" void func_0010F480(func_0010F480_Object *object) {
    func_0010F480_Callback *callback = object->callback;
    callback->call((char *)object + callback->offset);
    object->field84 = 0;
    object->field80 = 0;
}
