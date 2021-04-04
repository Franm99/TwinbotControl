from simple_pid import PID


class PIDController():
    def __init__(self, P, I, D, sample_time, output_limits):

        self.Px, self.Py, self.Pz = P[0], P[1], P[2]
        self.Ix, self.Iy, self.Iz = I[0], I[1], I[2]
        self.Dx, self.Dy, self.Dz = D[0], D[1], D[2]

        self.sample_time = sample_time
        self.output_lims = output_limits

        self.pidx = PID(self.Px, self.Ix, self.Dx,
                        self.sample_time, output_limits=self.output_lims)
        self.pidy = PID(self.Py, self.Iy, self.Dy,
                        self.sample_time, output_limits=self.output_lims)
        self.pidz = PID(self.Pz, self.Iz, self.Dz,
                        self.sample_time, output_limits=self.output_lims)

    def setpoint(self, ref):
        self.pidx.setpoint = ref[0]
        self.pidy.setpoint = ref[1]
        self.pidz.setpoint = ref[2]

    def __call__(self, actual_pos):
        vx = self.pidx(actual_pos[0])
        vy = self.pidy(actual_pos[1])
        vz = self.pidz(actual_pos[2])
        return vx, vy, vz


