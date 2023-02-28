for f in $(ls variable_sites/*txt)
do
  echo python make_invariable.py $f
done
