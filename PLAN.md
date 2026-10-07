This project is meant to manage backups from my arg eon host to my other network-mounted hard drives in my rackmate pi cluster.  It is the first step for me into having data redundancy for my critical systems.  I'd hate to lose all the movies I've encoded, and all the files I've generated.  This is meant to help prevent that.

The config will be filled with jobs of this format:
```json
{
  "jobs": [
    {
      "id": "fromid",
      "interval": "60",
      "max": "3",
      "target": "/home/jacob/jg_projects/dir_backups/_from",
      "destination": "/home/jacob/jg_projects/dir_backups/_to",
      "options": {
        "cpignore": [
          "ignore",
          "ignoree.txt"
        ]
      }
    }
  ]
}
```

TODO:

I have the zip archives working.  Now, I need to get the ignore setting working

The system  needs to be able to remember previous archives made for each job, so it can delete them.

Then, we need to build an auto-deploy script runnable from github!