###Mappers

where2Move.py uses mrjob and runs locally but not on EMR

corrMapper.py runs as a mapper task, for example:

	-files s3://kelley-w205/Project/corrMapper.py -mapper corrMapper.py -reducer NONE -input s3://kelley-w205/Project/Input/tags64.txt -output s3://kelley-w205/Project/Output/8dec2014_5/

This works for 2 core instances, medium, large, or xlarge but not for more

