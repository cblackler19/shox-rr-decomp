extern "C" void func_001117C8(char** destination, const char* source)
{
    __builtin_memcpy(*destination, source, 4);
    *destination += 4;
}