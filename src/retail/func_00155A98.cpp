struct ObjectAt1C { unsigned char padding[0x1C]; int value; };
extern "C" void func_00155AB8(ObjectAt1C*);
extern "C" void func_00155A98(ObjectAt1C* object) {
    object->value = 0;
    func_00155AB8(object);
}
