struct Initializable { int first; int second; int third; void* resource; };
extern char D_0044FF90[];
extern "C" Initializable* func_001590C0(Initializable* object) {
    object->first = 0;
    object->second = 0;
    object->third = 0;
    object->resource = D_0044FF90;
    return object;
}
