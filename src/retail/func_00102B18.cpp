struct State_481EA8 { unsigned int initialized; unsigned int reserved[3]; };
extern "C" State_481EA8 D_481EA8;
extern "C" unsigned char D_00446578[16];
extern "C" void func_002671E0(State_481EA8 *, const void *);
extern "C" State_481EA8 *func_00102B18(void) {
    if (!D_481EA8.initialized)
        func_002671E0(&D_481EA8, D_00446578);
    return &D_481EA8;
}
