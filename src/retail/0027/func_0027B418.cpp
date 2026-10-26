struct Result {
    unsigned short value;
};

extern "C" void func_002881D0(Result *);

extern "C" unsigned int func_0027B418()
{
    Result result;
    func_002881D0(&result);
    return result.value;
}
