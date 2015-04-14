# ELF_callgraph
Generate function call graph from powerpc ELF.

# User guide
powerpc-linux-gnu-objdump -d example.elf | python cg.py | dot -Tpng > cg.png && eog cg.png

or

sh gen_cg_pdf.sh input output(.pdf)
