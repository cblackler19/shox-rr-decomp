struct InitArgs {
    int value;
    int unused[5];
    int option;
};

extern "C" void func_002393C8(InitArgs *);

extern "C" void func_00239B30(InitArgs *args, int option, int value)
{
    args->value = value;
    args->option = option;
    func_002393C8(args);
}
