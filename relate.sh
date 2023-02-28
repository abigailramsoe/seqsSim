

basedir=results
mkdir -p $basedir/relate/
blist=$basedir/relate/bamlist.txt
ls bam/*.bam > $blist

python variable_pos_list.py > pos
refpos=pos
/projects/lundbeck/apps/angsd/angsd sites index $refpos
/projects/lundbeck/apps/angsd/angsd -checkBamHeaders 0 -b $blist -gl 1 -doMajorMinor 1  -doMaf 1 -minMapQ 30 -minQ 20 -minMaf 0.05 -doGlf 3 -nThreads 12 -sites $refpos -out $basedir/relate/allbams

zcat $basedir/relate/allbams.mafs.gz | cut -f5 |sed 1d > $basedir/relate/freq_from_pop


n=$(wc -l $blist|cut -f1 -d" ")
/projects/korneliussen/apps/ngsRelate/ngsRelate -g $basedir/relate/allbams.glf.gz -n $n -f $basedir/relate/freq_from_pop -O $basedir/relate/ngsresults
