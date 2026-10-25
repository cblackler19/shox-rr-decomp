typedef unsigned int uint128 __attribute__((mode(TI)));
extern "C" void func_00128AE8(void *source, void *destination) {
    *(uint128 *)destination = *(uint128 *)((char *)source + 144);
}
