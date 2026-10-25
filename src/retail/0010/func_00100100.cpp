typedef char* va_list;
#define va_start(list, last) ((list) = (char*)__builtin_next_arg(last) - 6 * sizeof(unsigned long long))

extern "C" void func_002CF118(void*, int, va_list);

extern "C" void func_00100100(void* format, int options, ...) {
    va_list arguments;
    va_start(arguments, options);
    func_002CF118(format, options, arguments);
}
