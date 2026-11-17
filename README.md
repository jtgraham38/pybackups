# pybackups: a service to back up your files 

`pybackups` is a python service designed to copy a folder an all its contents to another directory.  I built it because on my home cluster, I have a large library of files sitting on a single logical volume, connected to multiple hosts via nfs.  If one of the drives goes bad, I will lose a ton of data.  But, I have other hard drives that I can copy those files to.  So that is what this script does.  It takes a configurable path to a directory, reads all its contents (With a configurable ignore list), and copies them into a zip archive at another configurable destination.  It does this on a configurable interval, and keeps a configurable number of the most recent zip backups.

## Installation
`pybackups` currently only supports debian and ubuntu based systems.  To install it, run

```bash
curl -sL https://raw.githubusercontent.com/jtgraham38/pybackups/main/scripts/install.sh | sudo bash   
```

This script will install the repo and configure it to run as a systemd service on your host.  It will install the repo to the `/opt/pybackups` directory, and will intitialize the `/etc/pybackups` directory to hold config, and the `/var/lib/pybackups` directory to hold state.

Test installation by running 

```bash
sudo systemctl status pybackups
```

If it worked, the service status should be `active (running)`.

### Pro tip

If you have python/pip/etc. installed, but cannot run it with sudo due to path issues, try 

```bash
curl -sL https://raw.githubusercontent.com/jtgraham38/pybackups/main/scripts/install.sh | sudo env PATH="$PATH" bash 
```


instead.

## Updating
To update the service to the latest version, simply run 

```bash
curl -sL https://raw.githubusercontent.com/jtgraham38/pybackups/main/scripts/update.sh | sudo bash   
```

This will pull the latest version of the service, and restart the service on your host, retaining existing config and state.

### Pro tip

If you have python/pip/etc. installed, but cannot run it with sudo due to path issues, try 

```bash
curl -sL https://raw.githubusercontent.com/jtgraham38/pybackups/main/scripts/update.sh | sudo env PATH="$PATH" bash 
```

instead.

## Uninstallation
To completely uninstall all trace of the service, run

```bash
curl -sL https://raw.githubusercontent.com/jtgraham38/pybackups/main/scripts/uninstall.sh | sudo bash   
```

This will remove the service, repo, state, and config files from your host.  `pybackups` will be gone without a trace.

### Pro tip

If you have python/pip/etc. installed, but cannot run it with sudo due to path issues, try 

```bash
curl -sL https://raw.githubusercontent.com/jtgraham38/pybackups/main/scripts/uninstall.sh | sudo env PATH="$PATH" bash  
```

instead.

## Configuration
By default, `pybackups` simply runs in the background, doing nothing.  To start making zip backups, you need to edit the config file.  This file is located at `/etc/pybackups/config.json`.  By default, it will contain a single `jobs` key set to an empty array.  You can add as many entries to this array as you desire.  To add copy jobs, simply add an entry to this array:

```json
{
    "jobs": [
        {
            "id": "<unique_id_here>",
            "target": "/home/<user>/path/to/file/you/want/to/backup",
            "destination": "/home/<user>/path/to/place/you/want/to/store/zip/backups",
            "interval": "60",
            "max": "3",
            "options": {
                "cpignore": [
                "ignore",
                "ignore.txt"
                ],
                "compression": 93,
                "allowZip64": true,
                "compresslevel": 3,
                "strict_timestamps": true
            }
        }
    ]
}
```

Let's look at the above config.  Firstly, to define a job, you need to give it an `id`, `interval`, `max`, `target`, `destination`, and `options` field.  These define the core of a backup job.

### `id`
`id` is simply a unique string used internally to track a job.  Just make it unique from all other jobs.

### `target`
`target` is the path to the directory that you want to back up.  It's contents will be included in the zip archives created at the `destination`.

### `destination`
`destination` is the path to the directory where you want to store the `.zip` copies of the `target` directory.  Ideally, this should be on a different physical disk than `target`.

### `interval`
`interval` specifies the number of seconds that should pass between each backup of the `target` to a `.zip` archive in the `destination`.  Note that the backup loop only runs every 60s, so intervals smaller than that will run just once every 60s.

### `max`
`max` is the number of rolling copies of `target` that should be kept as `.zip` archives in the `destination`.  When this number is exceeded, the oldest archive will be deleted.  This can combine with `interval` to do neat things like keeping a rolling backup of the last three weeks of the state of a given folder.

### `options`
`options` is where custom arguments to the job are passed.  Right now, just two entrie is required (though more may be added in the future).  `cpignore` allows the user to specify files and directories to exclude from the backup archive.  It works similarly to a `.gitignore` file, and serves a similar purpose: say you want to backup a folder, but exclude one (or more) large but unneeded subfolder.  This is how you do that.  `compression`, `allowZip64`, `compresslevel`, `strict_timestamps`, and `metadata_encoding` are fields for controlling settings of the zip archive, which you can read about in the official [zipfile.ZipFile documentation](https://docs.python.org/3.11/library/zipfile.html).  I will briefly list the possible values for them below:

- `compression`: `0` (`ZIP_STORED`), `8` (`ZIP_DEFLATED`), `12` (`ZIP_BZIP2`), `14` (`ZIP_LZMA`), and `93` (`ZIP_ZSTANDARD`).  Default `0` (`ZIP_STORED`).
- `allowZip64`: `true` or `false`.  Default `True`.
- `compressionlevel`: when `compression=8`, an integer from `0` to `9`.  When `compression=12`, an integer from `1` to `9`.  For `compression=93`, an integer from `-131072` to `22`.  Otherwise, it has no effect. Default `None`.
- `strict_timestamps`: `true` or `false`. Default `True`.
- `metadata_encoding`: just see the docs.  Default `None`.

### Zip Settings for Different Folders

For backing up folders, you should usually only ever need to touch a few of these.  In general, leaving `allowZip64=true` can't hurt.  For `compression`, generally a value of `93` (`ZIP_ZSTANDARD`) is a good default, with `compressionlevel=3` a sensible default.  `compression=8` is better when integration with older tools is needed.  In general, a higher `compressionlevel` will take longer to run, but could also result in a tighter compression (less space used).

What you should use depends on the type of files in your backup.  If you have a lot of video/audio, which is already tightly compressed by default, simply use `compression=0`.  If you have a large folder containing many repositories and git histories, we can save space there, so using `compression=93` and `compressionlevel=3` makes sense.  The best advice is to learn what these variables do, make a judgement call with your jobs, and adjust based on how thing work until you find your ideal ratio of compression to speed.

## Conclusion
`pybackups` is meant to help you make... backups of your data using... python.  Hence the name.  Once again, it is designed to make it easy to have copies of folders on a separate disk, just in case one disk fails.  Therefore, ideally, you would be copying from one mounted disk to another, like `target=/mnt/sda1/folder`, and `destination=/mnt/sdb1/backups`.  This is an open-source tool that I use for personal projects, so what you see is what you get.  There may be bugs, so if you are worried about it, audit the code, or use a more robust, battle-tested tool.  I also built this as an exercise to make sure I can still code in the age of ai :D.  Good luck and enjoy!

[Jacob Graham](https://jacob-t-graham.com)