struct Inner_0026F488 { float scale; int first; int second; };
struct Outer_0026F488 { int unused; Inner_0026F488 *inner; };
extern "C" void func_0026BFC8(float, int, int);
extern "C" void func_0026F488(Outer_0026F488 *object)
{
    Inner_0026F488 *inner = object->inner;
    func_0026BFC8(inner->scale, inner->first, inner->second);
}
