typedef unsigned int Quadword __attribute__((mode(TI)));

extern "C" void func_00128B10(void* object, Quadword* output)
{
    *output = *(Quadword*)((char*)object + 0x40);
}
