// Evolve the scalar wave equation with Dirichlet boundaries

/* This kernel is very short. To run efficiently, probably the
   following optimizations need to occur:
   - Vectorization (with the device's natural vector length)
   - Maybe: Loop unrolling with small 3D blocks
   - Small explicit 3D loops (to amortize stencil loads, aka "loop
     blocking")
   - Multi-threading (aka parallelization)
   - Hoist setup operations (mostly integer operations) out of the
     kernel loop
   None of these are implemented explicitly here. We could provide
   several optimized versions, and then compare with pocl's
   capabilities.
 */

// #ifdef cl_khr_fp64
#pragma OPENCL EXTENSION cl_khr_fp64 : enable
// #endif

typedef struct grid_t {
  double dt;         // time step
  double dx, dy, dz; // resolution
  int ai, aj, ak;    // allocated size
  int ni, nj, nk;    // used size
} grid_t;

kernel void scalarwave(global double *restrict phi,
                       global const double *restrict phi_p,
                       global const double *restrict phi_p_p,
                       constant grid_t *restrict grid) {
  /* printf("dt=%g\n", grid->dt); */
  /* printf("dxyz=[%g,%g,%g]\n", grid->dx, grid->dy, grid->dz); */
  /* printf("aijk=[%d,%d,%d]\n", grid->ai, grid->aj, grid->ak); */
  /* printf("nijk=[%d,%d,%d]\n", grid->ni, grid->nj, grid->nk); */

  double dt = grid->dt;

  double dx = grid->dx;
  double dy = grid->dy;
  double dz = grid->dz;

  double dt2 = pown(dt, 2);

  double idx2 = pown(dx, -2);
  double idy2 = pown(dy, -2);
  double idz2 = pown(dz, -2);

  size_t ai = grid->ai;
  size_t aj = grid->aj;
  size_t ak = grid->ak;

  size_t ni = grid->ni;
  size_t nj = grid->nj;
  size_t nk = grid->nk;

  size_t di = 1;
  size_t dj = di * ai;
  size_t dk = dj * aj;

  /* printf("work_dim     =%u\n", get_work_dim()); */
  /* printf("global_size  =[%zu,%zu,%zu]\n", get_global_size(0), get_global_size(1), get_global_size(2)); */
  /* printf("global_id    =[%zu,%zu,%zu]\n", get_global_id(0), get_global_id(1), get_global_id(2)); */
  /* printf("local_size   =[%zu,%zu,%zu]\n", get_local_size(0), get_local_size(1), get_local_size(2)); */
  /* printf("local_id     =[%zu,%zu,%zu]\n", get_local_id(0), get_local_id(1), get_local_id(2)); */
  /* printf("num_groups   =[%zu,%zu,%zu]\n", get_num_groups(0), get_num_groups(1), get_num_groups(2)); */
  /* printf("group_id     =[%zu,%zu,%zu]\n", get_group_id(0), get_group_id(1), get_group_id(2)); */
  /* printf("global_offset=[%zu,%zu,%zu]\n", get_global_offset(0), get_global_offset(1), get_global_offset(2)); */

  size_t i = get_global_id(0);
  size_t j = get_global_id(1);
  size_t k = get_global_id(2);

  // If outside the domain, do nothing
  if (__builtin_expect(i >= ni || j >= nj || k >= nk, false))
    return;

  size_t ind3d = di * i + dj * j + dk * k;

  if (__builtin_expect(i == 0 || j == 0 || k == 0 || i == ni - 1 ||
                           j == nj - 1 || k == nk - 1,
                       false)) {
    // Boundary condition

    phi[ind3d] = 0.0;

  } else {
    // Scalar wave equation

    phi[ind3d] =
        2.0 * phi_p[ind3d] - phi_p_p[ind3d] +
        dt2 * ((phi_p[ind3d - di] - 2.0 * phi_p[ind3d] + phi_p[ind3d + di]) *
                   idx2 +
               (phi_p[ind3d - dj] - 2.0 * phi_p[ind3d] + phi_p[ind3d + dj]) *
                   idy2 +
               (phi_p[ind3d - dk] - 2.0 * phi_p[ind3d] + phi_p[ind3d + dk]) *
                   idz2);
  }
}
