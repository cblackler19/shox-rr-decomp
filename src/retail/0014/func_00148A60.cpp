struct Data_148A60 {
    unsigned char unused[192];
    float first;
    float second;
};
extern "C" float func_0013F0E8(int, float, float, float);
extern "C" void func_00148A60(Data_148A60 *data, float value)
{
    func_0013F0E8(1, data->first, data->second, value);
}
