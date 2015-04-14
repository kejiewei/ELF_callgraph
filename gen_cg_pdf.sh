#!/bin/sh
if [ $# -ne 2 ]
then
    echo "Usage: sh gen_cg_pdf input output(.pdf)"
    exit 1
fi

input=$1
output=$2
powerpc-linux-gnu-objdump -d $input | python cg.py > $input.cg
cat $input.cg | grep -v 'allocator'| grep -v 'Node' | grep -v '~' | grep -v 'operator' | sed '1d' | sed '$d'| sort | uniq | sed '1i digraph g {'| sed '$a }' | dot -Tpdf > $output
mv $input.cg ./
