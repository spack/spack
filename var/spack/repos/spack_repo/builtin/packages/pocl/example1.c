/* example1 - Simple example from OpenCL specification.

   Copyright (c) 2011 Universidad Rey Juan Carlos

   Permission is hereby granted, free of charge, to any person
   obtaining a copy of this software and associated documentation
   files (the "Software"), to deal in the Software without
   restriction, including without limitation the rights to use, copy,
   modify, merge, publish, distribute, sublicense, and/or sell copies
   of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be
   included in all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
*/

#include <CL/opencl.h>
#include <poclu.h>
#include <stdio.h>
#include <stdlib.h>

#define N 128

void delete_memobjs(cl_mem *memobjs, int n) {
  for (int i = 0; i < n; ++i)
    clReleaseMemObject(memobjs[i]);
}

int exec_dot_product_kernel(const char *program_source, int n, cl_float4 *srcA,
                            cl_float4 *srcB, cl_float *dst) {
  cl_context context = poclu_create_any_context();
  if (context == (cl_context)0)
    return -1;

  // get the list of GPU devices associated with context
  size_t cb;
  clGetContextInfo(context, CL_CONTEXT_DEVICES, 0, NULL, &cb);
  cl_device_id *devices = malloc(cb);
  clGetContextInfo(context, CL_CONTEXT_DEVICES, cb, devices, NULL);

  // create a command-queue
  cl_command_queue cmd_queue =
      clCreateCommandQueue(context, devices[0], 0, NULL);
  if (cmd_queue == 0) {
    clReleaseContext(context);
    free(devices);
    return -1;
  }

  // don't know why this is necessary
  for (int i = 0; i < n; ++i) {
    poclu_bswap_cl_float_array(devices[0], &srcA[i], 4);
    poclu_bswap_cl_float_array(devices[0], &srcB[i], 4);
  }

  // allocate the buffer memory objects
  cl_mem memobjs[3];

  memobjs[0] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
                              sizeof(cl_float4) * n, srcA, NULL);
  if (memobjs[0] == 0) {
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  memobjs[1] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
                              sizeof(cl_float4) * n, srcB, NULL);
  if (memobjs[1] == 0) {
    delete_memobjs(memobjs, 1);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  memobjs[2] = clCreateBuffer(context, CL_MEM_READ_WRITE, sizeof(cl_float) * n,
                              NULL, NULL);
  if (memobjs[2] == 0) {
    delete_memobjs(memobjs, 2);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  // create the program
  cl_program program =
      clCreateProgramWithSource(context, 1, &program_source, NULL, NULL);
  if (program == 0) {
    delete_memobjs(memobjs, 3);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  // build the program
  cl_int err = clBuildProgram(program, 0, NULL, NULL, NULL, NULL);
  if (err != CL_SUCCESS) {
    delete_memobjs(memobjs, 3);
    clReleaseProgram(program);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  // create the kernel
  cl_kernel kernel = clCreateKernel(program, "dot_product", NULL);
  if (kernel == 0) {
    delete_memobjs(memobjs, 3);
    clReleaseProgram(program);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  // set the args values
  err = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void *)&memobjs[0]);
  err |= clSetKernelArg(kernel, 1, sizeof(cl_mem), (void *)&memobjs[1]);
  err |= clSetKernelArg(kernel, 2, sizeof(cl_mem), (void *)&memobjs[2]);

  if (err != CL_SUCCESS) {
    delete_memobjs(memobjs, 3);
    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  // set work-item dimensions
  size_t global_work_size[1];
  global_work_size[0] = n;
  size_t local_work_size[1];
  local_work_size[0] = 128;

  // execute kernel
  err = clEnqueueNDRangeKernel(cmd_queue, kernel, 1, NULL, global_work_size,
                               local_work_size, 0, NULL, NULL);
  if (err != CL_SUCCESS) {
    delete_memobjs(memobjs, 3);
    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  // read output image
  err = clEnqueueReadBuffer(cmd_queue, memobjs[2], CL_TRUE, 0,
                            n * sizeof(cl_float), dst, 0, NULL, NULL);
  if (err != CL_SUCCESS) {
    delete_memobjs(memobjs, 3);
    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(cmd_queue);
    clReleaseContext(context);
    return -1;
  }

  for (int i = 0; i < n; ++i) {
    poclu_bswap_cl_float_array(devices[0], &dst[i], 1);
    poclu_bswap_cl_float_array(devices[0], &srcA[i], 4);
    poclu_bswap_cl_float_array(devices[0], &srcB[i], 4);
  }

  free(devices);

  // release kernel, program, and memory objects
  delete_memobjs(memobjs, 3);
  clReleaseKernel(kernel);
  clReleaseProgram(program);
  clReleaseCommandQueue(cmd_queue);
  clReleaseContext(context);

  // success
  return 0;
}

int main(void) {
  const char *source = "__kernel void dot_product(\n"
                       "  __global const float4 *a,\n"
                       "  __global const float4 *b,\n"
                       "  __global float *c)\n"
                       "{\n"
                       "  int gid = get_global_id(0);\n"
                       "  float4 prod = a[gid] * b[gid];\n"
                       "  c[gid] = prod.x + prod.y + prod.z + prod.w;\n"
                       "}\n";

  cl_float4 *srcA = malloc(N * sizeof(cl_float4));
  cl_float4 *srcB = malloc(N * sizeof(cl_float4));
  cl_float *dst = malloc(N * sizeof(cl_float));

  for (int i = 0; i < N; ++i) {
    srcA[i].s[0] = (cl_float)i;
    srcA[i].s[1] = (cl_float)i;
    srcA[i].s[2] = (cl_float)i;
    srcA[i].s[3] = (cl_float)i;
    srcB[i].s[0] = (cl_float)i;
    srcB[i].s[1] = (cl_float)i;
    srcB[i].s[2] = (cl_float)i;
    srcB[i].s[3] = (cl_float)i;
  }

  if (exec_dot_product_kernel(source, N, srcA, srcB, dst)) {
    printf("Error running the tests\n");
    return -1;
  }

  for (int i = 0; i < 4; ++i) {
    printf("(%f, %f, %f, %f) . (%f, %f, %f, %f) = %f\n", srcA[i].s[0],
           srcA[i].s[1], srcA[i].s[2], srcA[i].s[3], srcB[i].s[0], srcB[i].s[1],
           srcB[i].s[2], srcB[i].s[3], dst[i]);
    if (srcA[i].s[0] * srcB[i].s[0] + srcA[i].s[1] * srcB[i].s[1] +
            srcA[i].s[2] * srcB[i].s[2] + srcA[i].s[3] * srcB[i].s[3] !=
        dst[i]) {
      printf("FAIL\n");
      return -1;
    }
  }

  printf("OK\n");
  return 0;
}
