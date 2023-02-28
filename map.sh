
for f in $(ls fq/*fq)
do
  echo "bwa mem fasta/reference_genome.fa $f -t 16 |samtools sort -m4G - > sam/$(basename $f .fq).bam"
done

for f in $(ls sam/*bam|cut -f1 -d.|sort -u)
do
  echo samtools merge bam/$(basename $f).bam $(ls $f*bam) -f -@4
done

for f in $(ls bam/*bam)
do
  samtools index $f
done |parallel
