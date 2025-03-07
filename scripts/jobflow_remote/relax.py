
from jobflow_remote.jobs.submit import submit_flow
from atomate2.vasp.jobs.core import RelaxMaker
from pymatgen.core import Structure
from atomate2.vasp.powerups import update_user_incar_settings, update_vasp_custodian_handlers


# construct a rock salt MgO structure
mgo_structure = Structure(
    lattice=[[0, 2.13, 2.13], [2.13, 0, 2.13], [2.13, 2.13, 0]],
    species=["Mg", "O"],
    coords=[[0, 0, 0], [0.5, 0.5, 0.5]],
)

flow = RelaxMaker().make(mgo_structure)

flow = update_user_incar_settings(flow, {"NCORE": 4, "ISPIN": 1, "ENCUT": 300, "ENAUG": 600, "NSW": 10})

res = {"nodes": 1, "ntasks":4, "time": "00:20:00"}
submit_flow(flow, worker="cecam", resources=res, exec_config="vasp_6.4.3_cecam")