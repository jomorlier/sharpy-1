import sharpy.utils.cout_utils as cout
from sharpy.presharpy.utils.settings import str2bool
from sharpy.utils.solver_interface import solver, BaseSolver

from tvtk.api import tvtk, write_data
import numpy as np
import os

@solver
class AeroGridPlot(BaseSolver):
    solver_id = 'AeroGridPlot'
    solver_type = 'postproc'
    solver_unsteady = False

    def __init__(self):
        pass

    def initialise(self, data):
        self.data = data
        self.settings = data.settings[self.solver_id]
        self.convert_settings()

    def run(self):
        # create folder for containing files if necessary
        if not os.path.exists(self.settings['route']):
            os.makedirs(self.settings['route'])
        self.plot_grid()
        cout.cout_wrap('...Finished', 1)
        return self.data

    def convert_settings(self):
        # try:
        #     self.settings['print_info'] = (str2bool(self.settings['print_info']))
        # except KeyError:
        #     self.settings['print_info'] = True
        #
        # try:
        #     self.settings['plot_shape'] = (str2bool(self.settings['plot_shape']))
        # except KeyError:
        #     self.settings['plot_shape'] = True
        #
        try:
            self.settings['route'] = (str2bool(self.settings['route']))
        except KeyError:
            cout.cout_wrap('AeroGridPlot: no location for figures defined, defaulting to ./output', 3)
            self.settings['route'] = './output'
        pass

    def plot_grid(self):
        for i_surf in range(self.data.grid.n_surf):
            filename = 'grid_%s_%03u' % (self.data.settings['SHARPy']['case'], i_surf)

            dims = self.data.grid.aero_dimensions[i_surf, :]
            coords = np.zeros(((dims[0]+1)*(dims[1]+1), 3))
            # conn = np.zeros((dims[0]*dims[1], 4), dtype=int)
            conn = []
            panel_id = np.zeros((dims[0]*dims[1],), dtype=int)
            normal = np.zeros((dims[0]*dims[1], 3))
            counter = -1
            for i_n in range(dims[1]+1):
                for i_m in range(dims[0]+1):
                    counter += 1
                    coords[counter, :] = self.data.grid.zeta[i_surf][:, i_m, i_n]

            counter = -1
            node_counter = -1
            for i_n in range(dims[1] + 1):
                for i_m in range(dims[0] + 1):
                    node_counter += 1
                    if i_n < dims[1] and i_m < dims[0]:
                        counter += 1
                    else:
                        continue

                    conn.append([node_counter + 0,
                                 node_counter + 1,
                                 node_counter + dims[0]+2,
                                 node_counter + dims[0]+1])
                    normal[counter, :] = self.data.grid.normals[i_surf][:, i_m, i_n]
                    panel_id[counter] = counter

            ug = tvtk.UnstructuredGrid(points=coords)
            ug.set_cells(tvtk.Quad().cell_type, conn)
            ug.cell_data.scalars = panel_id
            ug.cell_data.scalars.name = 'panel_id'
            ug.cell_data.vectors = normal
            ug.cell_data.vectors.name = 'normal'
            ug.point_data.scalars = np.arange(0, coords.shape[0])
            ug.point_data.scalars.name = 'point_id'
            write_data(ug, filename)
        pass

