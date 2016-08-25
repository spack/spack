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

void exec_scalarwave_kernel(const char *program_source, cl_double *phi,
                            const cl_double *phi_p, const cl_double *phi_p_p,
                            const grid_t *grid) {
  static bool initialised = false;
  static cl_context context;
  static cl_command_queue cmd_queue;
  static cl_program program;
  static cl_kernel kernel;

  cl_int ierr;

  if (!initialised) {
    initialised = true;

    fprintf(stderr, "clGetPlatformIDs\n");
    cl_uint num_platforms;
    ierr = clGetPlatformIDs(0, NULL, &num_platforms);
    assert(!ierr);
    fprintf(stderr, "   num_platforms=%u\n", (unsigned)num_platforms);
    assert(num_platforms);
    cl_platform_id *platforms = malloc(num_platforms * sizeof(cl_platform_id));
    assert(platforms);
    ierr = clGetPlatformIDs(num_platforms, platforms, NULL);
    assert(!ierr);
    cl_platform_id platform = platforms[0];

    fprintf(stderr, "clGetDeviceIDs\n");
    cl_uint num_devices;
    ierr = clGetDeviceIDs(platform, CL_DEVICE_TYPE_ALL, 0, NULL, &num_devices);
    assert(!ierr);
    fprintf(stderr, "   num_devices=%u\n", (unsigned)num_devices);
    assert(num_devices);
    cl_device_id *devices = malloc(num_devices * sizeof(cl_device_id));
    assert(devices);
    ierr = clGetDeviceIDs(platform, CL_DEVICE_TYPE_ALL, num_devices, devices,
                          NULL);
    assert(!ierr);
    cl_device_id device = devices[0];

    fprintf(stderr, "clCreateContext\n");
    cl_context_properties properties[] = {
        CL_CONTEXT_PLATFORM, /*(cl_context_properties)*/ platforms, 0};
    cl_context context =
        clCreateContext(properties, num_devices, devices, NULL, NULL, NULL);
    assert(context);

    fprintf(stderr, "clCreateCommandQueue\n");
    cmd_queue = clCreateCommandQueue(context, device, 0, NULL);
    assert(cmd_queue);

    fprintf(stderr, "clCreateProgramWithSource\n");
    program = clCreateProgramWithSource(
        context, 1, /*(const char **)*/ &program_source, NULL, NULL);
    assert(program);

    fprintf(stderr, "clBuildProgram\n");
    ierr = clBuildProgram(program, 0, NULL, NULL, NULL, NULL);
    assert(!ierr);

    fprintf(stderr, "clCreateKernel\n");
    kernel = clCreateKernel(program, "scalarwave", NULL);
    assert(kernel);

    free(platforms);
    free(devices);
  }

  size_t npoints = grid->ai * grid->aj * grid->ak;
  cl_mem mem_phi =
      clCreateBuffer(context, 0, npoints * sizeof(cl_double), NULL, NULL);
  assert(mem_phi);
  cl_mem mem_phi_p = clCreateBuffer(context, CL_MEM_COPY_HOST_PTR,
                                    npoints * sizeof(cl_double), phi_p, NULL);
  assert(mem_phi_p);
  cl_mem mem_phi_p_p =
      clCreateBuffer(context, CL_MEM_COPY_HOST_PTR, npoints * sizeof(cl_double),
                     phi_p_p, NULL);
  assert(mem_phi_p_p);
  cl_mem mem_grid =
      clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
                     sizeof(grid_t), grid, NULL);
  assert(mem_grid);

  ierr = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mem_phi);
  assert(!ierr);
  ierr = clSetKernelArg(kernel, 1, sizeof(cl_mem), &mem_phi_p);
  assert(!ierr);
  ierr = clSetKernelArg(kernel, 2, sizeof(cl_mem), &mem_phi_p_p);
  assert(!ierr);

  ierr = clSetKernelArg(kernel, 3, sizeof(cl_mem), &mem_grid);
  assert(!ierr);

  size_t global_work_size[3] = {grid->ai, grid->aj, grid->ak};
  size_t local_work_size[3] = {GRID_GRANULARITY, GRID_GRANULARITY,
                               GRID_GRANULARITY};

  ierr = clEnqueueNDRangeKernel(cmd_queue, kernel, 3, NULL, global_work_size,
                                local_work_size, 0, NULL, NULL);
  assert(!ierr);

  ierr = clFinish(cmd_queue);
  assert(!ierr);

  ierr = clEnqueueReadBuffer(cmd_queue, mem_phi, CL_TRUE, 0,
                             npoints * sizeof(cl_double), phi, 0, NULL, NULL);
  assert(!ierr);

  ierr = clReleaseMemObject(mem_phi);
  assert(!ierr);
  ierr = clReleaseMemObject(mem_phi_p);
  assert(!ierr);
  ierr = clReleaseMemObject(mem_phi_p_p);
  assert(!ierr);
  ierr = clReleaseMemObject(mem_grid);
  assert(!ierr);
}

#define ALPHA 0.5 // CFL factor
#define NT 4      // time steps
#define NX 17     // grid size

// Round up to next multiple of GRID_GRANULARITY
static int roundup(int nx) {
  return (nx + GRID_GRANULARITY - 1) / GRID_GRANULARITY * GRID_GRANULARITY;
}

int main(void) {
  fprintf(stderr, "scalarwave\n");

  FILE *source_file = fopen("scalarwave.cl", "r");
  assert(source_file);

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
  for (ptrdiff_t k = 0; k < NX; ++k) {
    for (ptrdiff_t j = 0; j < NX; ++j) {
      for (ptrdiff_t i = 0; i < NX; ++i) {
        double t0 = 0.0;
        double t1 = -grid.dt;
        double x = i * grid.dx;
        double y = j * grid.dy;
        double z = k * grid.dz;
        ptrdiff_t ind3d = i + grid.ai * (j + grid.aj * k);
        phi[ind3d] = sin(kx * x) * sin(ky * y) * sin(kz * z) * cos(omega * t0);
        phi_p[ind3d] =
            sin(kx * x) * sin(ky * y) * sin(kz * z) * cos(omega * t1);
      }
    }
  }

  // Take some time steps
  for (ptrdiff_t n = 0; n < NT; ++n) {
    printf("Time step %td: t=%g\n", n + 1, (n + 1) * grid.dt);

    // Cycle time levels
    {
      cl_double *tmp = phi_p_p;
      phi_p_p = phi_p;
      phi_p = phi;
      phi = tmp;
    }

    // TODO: We allocate the buffers each time, which is slow. But
    // then, we only want to test correctness, not performance. (Yet?)
    exec_scalarwave_kernel(source, phi, phi_p, phi_p_p, &grid);
  } // for n

  printf("Result:\n");
  for (ptrdiff_t i = 0; i < NX; ++i) {
    ptrdiff_t j = i;
    ptrdiff_t k = i;
    double x = grid.dx * i;
    double y = grid.dy * j;
    double z = grid.dz * k;
    ptrdiff_t ind3d = i + grid.ai * (j + grid.aj * k);

    printf("   phi[%-6g,%-6g,%-6g] = %g\n", x, y, z, phi[ind3d]);
  }

  printf("Done.\n");

  free(source);
  free(phi);
  free(phi_p);
  free(phi_p_p);

  return 0;
}
