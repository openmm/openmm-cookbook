import openmm
import openmm.app
from openmm import unit
from nglview import NGLWidget, register_backend
import uuid
from nglview.base_adaptor import Structure, Trajectory
import numpy as np


def visualize(top, pos) -> NGLWidget:
    traj = OpenMMTrajectory(top, pos)

    widget = NGLWidget()
    widget.add_trajectory(traj)
    return widget


@register_backend("openmm")
class OpenMMTrajectory(Trajectory, Structure):
    def __init__(self, topology, positions):
        positions = np.asarray(positions) / unit.nanometer

        if positions.ndim == 2:
            positions = positions[np.newaxis, ...]
        elif positions.ndim == 3:
            positions = positions
        else:
            raise ValueError(
                f"positions should have 2 or 3 dimensions (had {positions.ndim})"
            )

        if positions.shape[1] != topology.getNumAtoms():
            raise ValueError(
                f"Should be a position for every atom in topology (expected shape (*, {topology.getNumAtoms()}, 3), found {positions.shape})"
            )

        if positions.shape[2] != 3:
            raise ValueError(
                f"Positions should be vectors in 3D space (expected shape (*, {topology.getNumAtoms()}, 3), found {positions.shape})"
            )

        self._top = topology
        self._pos = positions

        self.ext = "pdb"
        self.params = {}
        self.id = str(uuid.uuid4())

    def get_coordinates(self, index):
        return self._pos[index]

    @property
    def n_frames(self):
        return self._pos.shape[0]

    def get_structure_string(self):
        from io import StringIO

        file = StringIO("")
        openmm.app.pdbfile.PDBFile.writeFile(
            topology=self._top,
            positions=self._pos[0],
            file=file,
            keepIds=True,
        )
        file.seek(0)
        return file.read()
