## Git-ETL assignment

Python version >= 3.8

### Local testing

Paste your username/credentials in ```configs/job_config.json``` file, then run the job:

```
spark-submit job_git_fetch_repos.py
```

### Notes

* This job intended to be run locally. 
For cluster deployment we need to package job's dependencies at least.
Even more likely, that in cluster environment we would read configs from database and write results to S3 or DB, 
so I believe packaging part is out of the scope of this assignment.
* You can provide any number of credentials in ```configs/job_config.json``` file, but be aware of API rate limiter. 
* Extract and transform steps are not separated, which is not great.
But I deliberately opt for git connector's abstraction in that tradeoff.
* I didn't include tests in order to keep things as simple as possible.
Believe me, I know how to write them if needed. :smile:

LMK if you have any questions!