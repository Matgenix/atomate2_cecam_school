from jobflow_remote.testing import add, add_sleep
from jobflow import Flow
from jobflow_remote.jobs.submit import submit_flow
from qtoolkit.core.data_objects import QResources


add_first = add_sleep(1, 2)
add_second = add_sleep(add_first.output, 2)

flow = Flow([add_first, add_second])

flow.update_metadata({"test": "add"})

# submit_flow(flow, worker="cecam_fe")
submit_flow(flow, worker="cecam", resources={"nodes": 1, "ntasks": 1, "time": "00:10:00", "cpus_per_task": 1})
# submit_flow(flow, worker="local_shell", project="test_project_q", resources=QResources())