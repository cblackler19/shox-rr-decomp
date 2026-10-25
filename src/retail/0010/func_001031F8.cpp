struct ProgressState {
    char padding[0x14];
    unsigned int limit;
    unsigned int id;
    unsigned int reserved;
    unsigned int value;
    unsigned int state;
};

extern "C" void func_00102DB0();

extern "C" int func_001031F8(ProgressState* object, unsigned int id, unsigned int value) {
    object->id = id;
    unsigned int limit = object->limit;
    object->state = 0;
    object->value = value;

    if (value < ((value + limit) & ~limit)) {
        unsigned int adjusted = value - 1;
        object->value = adjusted - limit;
    }

    func_00102DB0();
    return 1;
}
