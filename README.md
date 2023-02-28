Fist run allelefreq.py 

```
python allelefreq.py
```

Change the number of sites, invariable sites and founders at the top 

```
# We want 100k variable sites with 1000 sites in between each one
sites = 100000
invariable_sites = 1000

# Start with four founders
founders = 4
```

This makes many things 
1. af.txt - a list of the allele frequencies (ancestral)
2. fasta/ancestral.fa and fasta/derived.fa - the ancestral and derived allele at each of the variable positions 
3. fasta/reference_genome.fa - the reference, with variable sites encoded as N 
4. variable_sites/{sample}.h[1,2].txt - the allele at each variable site for each sample, per haplotype 

Then for each variable site run make_inveriable.py 

```
for f in $(ls variable_sites/*)
do
  python make_invariable.py $f
done
```

This makes fasta files in final_fasta/, one for each individual and each haplotype. 

Use these as input to NGSNGS (change coverage in this step to investigate affect of that)
```
for fa in $(ls final_fasta/*fa)
do
  echo /home/dlm551/contamination/NGSNGS/ngsngs -i $fa -c 5 -f fq -l 100 -seq SE -t 5 -q1 /home/dlm551/contamination/NGSNGS/Test_Examples/AccFreqL150R1.txt -o fq/$(basename $fa .fa)
done
```

Now we have fastq files. We map them and merge the haplotypes together.
```
for f in $(ls fq/*fq)
do
  echo "bwa mem fasta/reference_genome.fa $f -t 16 |samtools sort -m4G - > sam/$(basename $f .fq).bam"
done|parallel 

for f in $(ls sam/*bam|cut -f1 -d.|sort -u)
do
  echo samtools merge bam/$(basename $f).bam $(ls $f*bam) -f -@4
done|parallel 

for f in $(ls bam/*bam)
do
  samtools index $f
done|parallel
```

Then we naively run ngsRelate 
```
bash relate.sh 
```
