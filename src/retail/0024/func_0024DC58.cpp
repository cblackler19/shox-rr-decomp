extern "C" void func_0024DC58(int *object, unsigned int index, int value)
{
    int *source = object + 9;
    source += index;
    int *destination = object;
    destination += index;
    int saved = *source;
    destination[13] = saved;
    *source = value;
}
