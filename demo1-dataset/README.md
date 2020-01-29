Demo1 Dataset
------

## Collection Method

### 1. from trashnet dataset:
trash under non-recyclable
all other categories under recyclablel

### 2. from general image datasets:
1000 imagenet images under non-recyclable
1000 food11 images under non-recyclable

### 3. from taco dataset:
crop the images by the given bounding boxes (see crop.py)
map taco categories to recyclable labels (see taco-taxonomy.csv, I did the recyclable annotation, not sure it's 100% correct)
filter out small images (png under 80k)

### 4. reserve some images from testing (see create-test.sh)

## Download link

<https://drive.google.com/file/d/1gzIpSyBq4y-k-UWI-u2e_VpFF_coNAm3/view?usp=sharing>

## Source Datasets

[trashnet](https://github.com/vasantvohra/TrashNet)
[imagenet](https://www.kaggle.com/lijiyu/imagenet)
[food11](https://www.kaggle.com/tohidul/food11)
[taco](http://tacodataset.org)
