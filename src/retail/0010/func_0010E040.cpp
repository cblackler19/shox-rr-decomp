extern "C" void func_0010E040(void* object)
{
    int* flags = (int*)((char*)object + 0x150);
    *flags &= -2;
    *flags &= -3;
    *flags &= -5;
}
