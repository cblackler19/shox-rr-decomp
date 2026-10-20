typedef int quad_t __attribute__((mode(TI)));
extern "C" void func_001445A0(void* destination, const void* source)
{
    *(quad_t*)((char*)destination + 0x70) = *(const quad_t*)source;
    *(int*)((char*)destination + 0x60) = 1;
}