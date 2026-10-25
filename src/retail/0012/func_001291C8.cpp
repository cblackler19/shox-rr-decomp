typedef unsigned int Quadword __attribute__((mode(TI)));

extern "C" void func_001291C8(void* object, float weight,
                              const Quadword* first, const Quadword* second)
{
    *(float*)((char*)object + 0xD0) = weight;
    *(Quadword*)((char*)object + 0xE0) = *first;
    *(Quadword*)((char*)object + 0xF0) = *second;
}
