for f in $(ls variable_sites/*)
do
  echo python make_invariable.py $f
done
