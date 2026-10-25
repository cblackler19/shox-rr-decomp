struct ObjectState
{
    void* resource;
    char padding[12];
    float enabled;
};
extern "C" char D_00454D30[] __attribute__((section(".rodata")));

extern "C" ObjectState* func_00178CA0(ObjectState* object)
{
    object->resource = D_00454D30;
    object->enabled = 1.0f;
    return object;
}