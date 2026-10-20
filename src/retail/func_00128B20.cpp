typedef unsigned int Quadword __attribute__((mode(TI)));

extern "C" void func_00128B20(void* object, const Quadword* input)
{
    *(Quadword*)((char*)object + 0x40) = *input;
}
