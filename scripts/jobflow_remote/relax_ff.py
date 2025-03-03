
from jobflow_remote.jobs.submit import submit_flow
from atomate2.forcefields.jobs import ForceFieldRelaxMaker
from pymatgen.core import Structure


# construct a rock salt MgO structure
mgo_structure = Structure(
    lattice=[[0, 2.13, 2.13], [2.13, 0, 2.13], [2.13, 2.13, 0]],
    species=["Mg", "O"],
    coords=[[0, 0, 0], [0.5, 0.5, 0.5]],
)

mgo_structure.perturb(0.1)

flow = ForceFieldRelaxMaker(force_field_name='CHGNet').make(mgo_structure)

res = {"nodes": 1, "ntasks":1, "time": "00:20:00"}
submit_flow(flow, worker="local_slurm", resources=res)