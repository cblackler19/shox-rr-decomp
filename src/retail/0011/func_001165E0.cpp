struct InitialValues {
    unsigned int header[2];
    float values[4];
    unsigned int state;
};

extern "C" void func_001165E0(InitialValues* object) {
    float zero = 0.0f;
    object->state = 0;
    object->values[3] = zero;
    object->values[2] = zero;
    object->values[1] = zero;
    object->values[0] = zero;
}
