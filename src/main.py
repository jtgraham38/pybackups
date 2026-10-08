from config import get_config, init_config, validate_config
from state import get_state, init_state, validate_state, save_state
from fs import zip_job, del_job, DelJobException
from datetime import datetime as dt
from datetime import timedelta
from collections import deque
import time


def py_backups():

    # init get and validate config
    init_config()
    config = get_config()
    validate_config(config)

    # init get and validate state
    init_state()
    state = get_state()
    validate_state(state)

    # execute a copy for each job from the target to the destination
    for job in config["jobs"]:
        interval = int(job["interval"])
        job_id = job["id"]
        max_backups = int(job["max"])
        target = job["target"]
        destination = job["destination"]
        options = job["options"]

        # ensure a state entry for the job exists
        if job_id not in state["jobs"]:
            state["jobs"][job_id] = {"backups": []}

        # first, determine if it is time for this job to run again, based on the job interval
        if len(state["jobs"][job_id]["backups"]) > 0:
            fmt_str = "%Y-%m-%d %H:%M:%S.%f"
            newest_backup_created_at = state["jobs"][job_id]["backups"][-1][
                "created_at"
            ]
            next_time_to_run = dt.strptime(
                newest_backup_created_at,
                fmt_str,
            ) + timedelta(seconds=interval)
            print(
                f"Time is now {dt.now()}, Job {job_id}'s next backup runs at {next_time_to_run}.  {dt.now() < next_time_to_run}"
            )
            if dt.now() < next_time_to_run:
                print(f"Not time to run job {job_id} yet, skipping!")
                continue

        # run a new zipjob to make the backup
        destination_file_path = zip_job(target, destination, options=options)

        # add backup to state.jobs.backups
        backups_q = deque()
        for x in state["jobs"][job_id]["backups"]:
            backups_q.append(x)
        backups_q.append(
            {"archive_file": str(destination_file_path), "created_at": str(dt.now())}
        )

        # check max_backups against length of state["jobs"][job_id]["backups"], and if there are x>0 more backups than that, delete the oldest x
        if len(backups_q) > max_backups:
            print(
                f"There are {len(backups_q)} for job {job_id}, and only {max_backups} are expected."
            )
            # the oldest backups will be held at the beginning of the list... so remove those ones first
            archives_to_remove = len(backups_q) - max_backups
            print(f"Removing {archives_to_remove} backups from job {job_id}")
            for i in range(archives_to_remove):
                backup_to_remove = backups_q.popleft()

                # delete the archive found at backup_to_remove['archive_file']
                try:
                    del_job(backup_to_remove["archive_file"])
                except DelJobException as e:
                    if not "Target path for job does not exist" in str(e):
                        raise DelJobException(str(e))

        # re-save the dequeue to the state
        state["jobs"][job_id]["backups"] = list(backups_q)

    # save state to file
    save_state(state)


if __name__ == "__main__":
    while True:
        # run the main app script every 60 seconds
        py_backups()
        time.sleep(60)
