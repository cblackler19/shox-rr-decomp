extern "C" int func_001AC158(void *, void *);

extern "C" int func_001CFC08(void *object)
{
    char *bytes = (char *)object;
    return func_001AC158(bytes + 1340, bytes + 5440);
}
