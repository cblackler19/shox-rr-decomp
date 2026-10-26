extern "C" int func_001AC300(void *, void *);

extern "C" int func_001CFBE8(void *object)
{
    char *bytes = (char *)object;
    return func_001AC300(bytes + 1340, bytes + 5440);
}
