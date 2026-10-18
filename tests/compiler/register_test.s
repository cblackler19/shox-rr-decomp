.set noreorder
.text
.globl register_test

register_test:
    addiu $29, $29, -16
    sq $31, 0($29)
    lq $31, 0($29)
    jr $31
    addiu $29, $29, 16
