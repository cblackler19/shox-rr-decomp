extern "C" char D_00446E60[] __attribute__((section(".rodata")));
extern "C" void func_001A6050(void* object);
extern "C" void func_0010C9B0(void* object, int initialize)
{
    void* resource = D_00446E60;
    *(void**)((char*)object + 240) = resource;
    *(void**)((char*)object + 136) = resource;
    *(void**)((char*)object + 20) = resource;
    if (initialize & 1)
        func_001A6050(object);
}