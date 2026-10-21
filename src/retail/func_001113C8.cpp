struct GridCell {
    unsigned int first;
    unsigned int second;
    GridCell* link;
    unsigned int last;
};

struct Grid {
    GridCell rows[8][29];
};

extern "C" void func_001113C8(Grid* grid, unsigned int source, unsigned int destination) {
    if (destination < 29 && source < 29) {
        unsigned int destinationOffset = destination * sizeof(GridCell);
        GridCell* sourceCell = &grid->rows[0][source];
        GridCell* destinationCell = reinterpret_cast<GridCell*>(reinterpret_cast<char*>(grid) + destinationOffset);
        for (unsigned int row = 0; row < 8; ++row) {
            if (sourceCell != destinationCell) {
                destinationCell->link = sourceCell;
            }
            sourceCell += 29;
            destinationCell += 29;
        }
    }
}
