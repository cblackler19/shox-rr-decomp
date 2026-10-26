struct Object_0026C6B0 { char *pointer; int flag; int value1; int value2; int value3; };
extern "C" char D_00468668[] __attribute__((section(".data")));
extern "C" Object_0026C6B0 *func_0026C6B0(Object_0026C6B0 *object, int first, int second)
{
    object->pointer = D_00468668;
    object->flag = 1;
    object->value1 = first;
    object->value3 = second;
    object->value2 = 0;
    return object;
}
