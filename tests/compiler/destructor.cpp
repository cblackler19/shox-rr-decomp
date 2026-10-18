
typedef unsigned int u32;

struct Object {
    unsigned char unknown_00[0x1C];
    void *resource;             // 0x1C
    unsigned char unknown_20[4];
    u32 active;                 // 0x24
};

extern "C" void release_resource(void *);
extern "C" void free_object(void *);
extern "C" unsigned char shox_vtable[];

extern "C" void test_destructor(Object *self, unsigned int flags)
{
    *(void **)((char *)self + 0x38) = shox_vtable;

    if (self->active != 0) {
        self->active = 0;
        release_resource(self->resource);
    }

    if ((flags & 1) != 0) {
        free_object(self);
    }
}
