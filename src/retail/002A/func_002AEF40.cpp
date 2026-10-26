struct Record
{
    unsigned short kind;
    unsigned short shortValue;
    unsigned int pointer;
    unsigned int value;
    unsigned int callback;
};

extern "C" unsigned int* func_002AEF40(Record* object, int, unsigned int* pointer, int,
                                         unsigned int shortValue, unsigned int callback,
                                         unsigned int value)
{
    object->kind = 0x424D;
    object->shortValue = (unsigned short)shortValue;
    object->pointer = (unsigned int)pointer;
    object->value = value;
    object->callback = callback;
    return pointer + 4;
}
