# minio-token-gen


---
# tutorials
## how-to-use 


```bash
$ python token-generation.py --help 
```

## where-to-use

1. connect to [MinIO](https://min.io/)

2. Connecting [LabelStudio](https://labelstud.io/) with [MinIO](https://min.io/). Store incoming files for labeling process in external service (object store).   
   [Sync data from external storage](https://labelstud.io/guide/storage) --> [S3](https://labelstud.io/guide/storage#Amazon-S3)

## upgrades 

 - use **get policy** from boto3 instead reading from local file 
   
