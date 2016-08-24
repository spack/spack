/* scalarwave - Scalar wave evolution */

#define _BSD_SOURCE // define M_PI
#define _DEFAULT_SOURCE

#include <CL/opencl.h>

#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define GRID_GRANULARITY 4

typedef struct grid_t {
  cl_double dt;         // time step
  cl_double dx, dy, dz; // resolution
  cl_int ai, aj, ak;    // allocated size
  cl_int ni, nj, nk;    // used size
} grid_t;

int exec_scalarwave_kernel(const char *program_source, cl_double *phi,
                           const cl_double *phi_p, const cl_double *phi_p_p,
                           const grid_t *grid) {
  static bool initialised = false;
  static cl_context context;
  static cl_command_queue cmd_queue;
  static cl_program program;
  static cl_kernel kernel;

  if (!initialised) {
    initialised = true;

    cl_uint num_platforms;
    clGetPlatformIDs(0, NULL, num_platforms);
    if (!num_platforms)
      return -1;
    cl_platform_id *platforms = malloc(num_platforms * sizeof(cl_platform_id));
    clGetPlatformIDs(num_platforms, platforms, NULL);

    cl_context_properties properties[] = {
        CL_CONTEXT_PLATFORM, (cl_context_properties)platforms[0], 0};
    cl_context context = clCreateContextFromType(properties, CL_DEVICE_TYPE_ALL,
                                                 NULL, NULL, NULL);
    if (!context)
      return -1;

    size_t ndevices;
    clGetContextInfo(context, CL_CONTEXT_DEVICES, 0, NULL, &ndevices);
    ndevices /= sizeof(cl_device_id);
    cl_device_id *devices = malloc(ndevices * sizeof(cl_device_id));
    clGetContextInfo(context, CL_CONTEXT_DEVICES,
                     ndevices * sizeof(cl_device_id), devices, NULL);

    cmd_queue = clCreateCommandQueue(context, devices[0], 0, NULL);
    if (!cmd_queue)
      return -1;

    program = clCreateProgramWithSource(
        context, 1, (const char **)&program_source, NULL, NULL);
    if (!program)
      return -1;

    int ierr;
    ierr = clBuildProgram(program, 0, NULL, NULL, NULL, NULL);
    if (ierr)
      return -1;

    kernel = clCreateKernel(program, "scalarwave", NULL);
    if (!kernel)
      return -1;

    free(platforms);
    free(devices);
  }

  size_t npoints = grid->ai * grid->aj * grid->ak;
  cl_mem mem_phi =
      clCreateBuffer(context, 0, npoints * sizeof(cl_double), NULL, NULL);
  if (!mem_phi)
    return -1;
  cl_mem mem_phi_p = clCreateBuffer(context, CL_MEM_COPY_HOST_PTR,
                                    npoints * sizeof(cl_double), phi_p, NULL);
  if (!mem_phi_p)
    return -1;
  cl_mem mem_phi_p_p =
      clCreateBuffer(context, CL_MEM_COPY_HOST_PTR, npoints * sizeof(cl_double),
                     phi_p_p, NULL);
  if (!mem_phi_p_p)
    return -1;
  cl_mem mem_grid =
      clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
                     sizeof(grid_t), grid, NULL);
  if (!mem_grid)
    return -1;

  int ierr;
  ierr = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mem_phi);
  if (ierr)
    return -1;
  ierr = clSetKernelArg(kernel, 1, sizeof(cl_mem), &mem_phi_p);
  if (ierr)
    return -1;
  ierr = clSetKernelArg(kernel, 2, sizeof(cl_mem), &mem_phi_p_p);
  if (ierr)
    return -1;
  ierr = clSetKernelArg(kernel, 3, sizeof(cl_mem), &mem_grid);
  if (ierr)
    return -1;

  size_t global_work_size[3] = {grid->ai, grid->aj, grid->ak};
  size_t local_work_size[3] = {GRID_GRANULARITY, GRID_GRANULARITY,
                               GRID_GRANULARITY};

  ierr = clEnqueueNDRangeKernel(cmd_queue, kernel, 3, NULL, global_work_size,
                                local_work_size, 0, NULL, NULL);
  if (ierr)
    return -1;

  ierr = clFinish(cmd_queue);
  if (ierr)
    return -1;

  ierr = clEnqueueReadBuffer(cmd_queue, mem_phi, CL_TRUE, 0,
                             npoints * sizeof(cl_double), phi, 0, NULL, NULL);
  if (ierr)
    return -1;

  clReleaseMemObject(mem_phi);
  clReleaseMemObject(mem_phi_p);
  clReleaseMemObject(mem_phi_p_p);
  clReleaseMemObject(mem_grid);
  /* clReleaseKernel(kernel); */
  /* clReleaseProgram(program); */
  /* clReleaseCommandQueue(cmd_queue); */
  /* clReleaseContext(context); */

  return 0;
}

#define ALPHA 0.5 // CFL factor
#define NT 4      // time steps
#define NX 17     // grid size

// Round up to next multiple of GRID_GRANULARITY
static int roundup(int nx) {
  return (nx + GRID_GRANULARITY - 1) / GRID_GRANULARITY * GRID_GRANULARITY;
}

int main(void) {
  FILE *source_file = fopen("scalarwave.cl", "r");
  assert(source_file != NULL && "scalarwave.cl not found!");

  fseek(source_file, 0, SEEK_END);
  size_t source_size = ftell(source_file);
  fseek(source_file, 0, SEEK_SET);

  char *source = malloc(source_size + 1);
  fread(source, source_size, 1, source_file);
  source[source_size] = '\0';

  fclose(source_file);

  grid_t grid;
  grid.dt = ALPHA / (NX - 1);
  grid.dx = grid.dy = grid.dz = 1.0 / (NX - 1);
  grid.ai = grid.aj = grid.ak = roundup(NX);
  grid.ni = grid.nj = grid.nk = NX;

  cl_double *restrict phi =
      malloc(grid.ai * grid.aj * grid.ak * sizeof(cl_double));
  cl_double *restrict phi_p =
      malloc(grid.ai * grid.aj * grid.ak * sizeof(cl_double));
  cl_double *restrict phi_p_p =
      malloc(grid.ai * grid.aj * grid.ak * sizeof(cl_double));

  // Set up initial data (TODO: do this on the device instead)
  printf("Initial condition: t=%g\n", 0.0);
  double kx = M_PI;
  double ky = M_PI;
  double kz = M_PI;
  double omega = sqrt(pow(kx, 2) + pow(ky, 2) + pow(kz, 2));
  for (int k = 0; k < NX; ++k) {
    for (int j = 0; j < NX; ++j) {
      for (int i = 0; i < NX; ++i) {
        double t0 = 0.0;
        double t1 = -grid.dt;
        double x = i * grid.dx;
        double y = j * grid.dy;
        double z = k * grid.dz;
        int ind3d = i + grid.ai * (j + grid.aj * k);
        phi[ind3d] = sin(kx * x) * sin(ky * y) * sin(kz * z) * cos(omega * t0);
        phi_p[ind3d] =
            sin(kx * x) * sin(ky * y) * sin(kz * z) * cos(omega * t1);
      }
    }
  }

  // Take some time steps
  for (int n = 0; n < NT; ++n) {
    printf("Time step %d: t=%g\n", n + 1, (n + 1) * grid.dt);

    // Cycle time levels
    {
      cl_double *tmp = phi_p_p;
      phi_p_p = phi_p;
      phi_p = phi;
      phi = tmp;
    }

    // TODO: We allocate the buffers each time, which is slow. But
    // then, we only want to test correctness, not performance. (Yet?)
    int ierr = exec_scalarwave_kernel(source, phi, phi_p, phi_p_p, &grid);
    assert(!ierr);

  } // for n

  printf("Result:\n");
  for (int i = 0; i < NX; ++i) {
    int j = i;
    int k = i;
    double x = grid.dx * i;
    double y = grid.dy * j;
    double z = grid.dz * k;
    int ind3d = i + grid.ai * (j + grid.aj * k);

    printf("   phi[%-6g,%-6g,%-6g] = %g\n", x, y, z, phi[ind3d]);
  }

  printf("Done.\n");

  free(source);
  return 0;
}
