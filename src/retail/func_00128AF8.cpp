typedef unsigned int Quadword __attribute__((mode(TI)));

extern "C" void func_00128AF8(void* object, const Quadword* input)
{
    Quadword value = *input;
    *(Quadword*)((char*)object + 0x90) = value;
    *(Quadword*)((char*)object + 0x130) = value;
    *(Quadword*)((char*)object + 0x140) = value;
}
