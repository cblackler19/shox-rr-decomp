struct ZeroGroup {
    unsigned int values[5];
};

struct ZeroObject {
    unsigned int header[2];
    ZeroGroup groups[4];
    unsigned int finalValue;
};

extern "C" void func_00109080(ZeroObject* object) {
    object->finalValue = 0;
    for (unsigned int i = 0; i < 4; ++i) {
        object->groups[i].values[0] = 0;
        object->groups[i].values[1] = 0;
        object->groups[i].values[2] = 0;
        object->groups[i].values[3] = 0;
        object->groups[i].values[4] = 0;
    }
}
