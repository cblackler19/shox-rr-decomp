extern "C" void func_002C9C94(void *destination, int value, int size);

extern "C" unsigned int D_00448F00[];
extern "C" unsigned int D_00448F48[];
extern "C" unsigned int D_00448F60[];
extern "C" unsigned int D_00448F80[];
extern "C" unsigned int D_00448FA0[];

struct DispatchData
{
    unsigned int value;
    void *callback;
};

extern "C" const DispatchData D_00448DF8 __attribute__((section(".rodata")));

struct DeviceState
{
    unsigned int zero0[5];
    unsigned int vtable;
    unsigned int zero18;
    unsigned int baseVtable;
    DispatchData dispatchData;
    DeviceState *owner;
    unsigned int flags;
    unsigned int zero30[5];
    unsigned int zero44;
    unsigned int zero48[6];
    unsigned int zero60;
    unsigned int vtable64;
    unsigned int vtable68;
    unsigned int vtable6C;
    unsigned int zero70[5];
    unsigned int zero84;
};

struct DeviceStateHeader
{
    unsigned int unknown0;
    unsigned int vtable;
    unsigned int dispatch0;
    unsigned int dispatch1;
    DeviceState *owner;
    unsigned int flags;
};

extern "C" DeviceState *func_00111930(DeviceState *state)
{
    DeviceStateHeader *header = (DeviceStateHeader *)((char *)state + 0x18);
    state->vtable = (unsigned int)D_00448F00;
    state->zero0[0] = 0;
    state->zero0[1] = 0;
    state->zero0[2] = 0;
    state->zero0[3] = 0;
    header->vtable = (unsigned int)D_00448F48;
    func_002C9C94((char *)state + 0x20, 0, 8);
    header->owner = 0;
    header->flags = 0;
    const DispatchData *dispatchSource = &D_00448DF8;
    DispatchData dispatchData = *dispatchSource;
    state->vtable64 = (unsigned int)D_00448FA0;
    state->vtable68 = (unsigned int)D_00448F80;
    state->vtable6C = (unsigned int)D_00448F60;
    state->zero30[0] = 0;
    state->zero30[1] = 0;
    state->zero30[2] = 0;
    state->zero30[3] = 0;
    state->zero30[4] = 0;
    state->zero48[0] = 0;
    state->zero48[1] = 0;
    state->zero48[2] = 0;
    state->zero48[3] = 0;
    state->zero48[4] = 0;
    state->zero48[5] = 0;
    state->dispatchData = dispatchData;
    header->owner = state;
    header->flags = (header->flags & 0x80000000u) | 0xAu;
    state->zero84 = 0;
    return state;
}
