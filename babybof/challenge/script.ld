OUTPUT_FORMAT(elf64-x86-64)
ENTRY(_start)

SECTIONS
{
  .bss 0x601010 :
  {
    KEEP(*(.bss));
  }
}
