extern "C" unsigned char D_00446518[];
extern "C" void func_00102B70(void *, unsigned int);
extern "C" void func_00239AE8(void *, int);
extern "C" void func_00102908(void *, int);
extern "C" void func_001A6050(void *);

struct Object_00102688 {
    char pad[600];
    void *descriptor;
};

extern "C" void func_00102688(Object_00102688 *object, unsigned int flags) {
    object->descriptor = D_00446518;
    func_00102B70((char *)object + 584, 2);
    func_00239AE8((char *)object + 24, 2);
    func_00102908(object, 2);
    if (flags & 1) {
        func_001A6050(object);
    }
}
