for dir in recyclable non-recyclable
do
    mkdir -p $2/$dir
    find $dir -type f | shuf | head -n $1 | while read line; do mv "$line" $2/$dir/; done
done
