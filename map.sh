
for f in $(ls fq/*fq)
do
  echo "bwa mem fasta/reference_genome.fa $f -t 16 |samtools sort -m4G - > sam/$(basename $f .fq).bam"
done
