extern "C" void func_001C15D8(float* object, float value) {
    float square = value * value;
    float result = square / object[0x6B];
    object[0] = value;
    object[0x6E] = result;
}
