
for fa in $(ls final_fasta/*fa)
do
  echo /home/dlm551/contamination/NGSNGS/ngsngs -i $fa -c 5 -f fq -l 100 -seq SE -t 5 -q1 /home/dlm551/contamination/NGSNGS/Test_Examples/AccFreqL150R1.txt -o fq/$(basename $fa .fa)
done
