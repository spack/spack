// Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
// Spack Project Developers. See the top-level COPYRIGHT file for details.
//
// SPDX-License-Identifier: (Apache-2.0 OR MIT)

#include <iostream>
#include <sstream>
#include <exception>
#include <functional>

#include <cassert>
#include <cstdint>
#include <cstdlib>

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <unistd.h>

#include <umap/umap.h>

namespace umaptest {

class TestException : public std::runtime_error {
  using std::runtime_error::runtime_error;
};

int memfd_create(std::string name, int flags) {
  int fd = syscall(__NR_memfd_create, name.c_str(), flags);
  if (fd < 0) {
    throw TestException("memfd_create failed: " + std::to_string(errno));
  }
  return fd;
}

class umap_test {
public:
  static const int TEST_FAIL = -1;
  static const int TEST_RO_PASS = 0;
  static const int TEST_RW_PASS = 1;
private:
  static const int PROT_RO = PROT_READ;
  static const int PROT_RW = PROT_READ | PROT_WRITE;
  int fd;
  void* umap_region;
  void* mmap_region;
  bool read_only;
  uint64_t region_size;

  void do_umap() {
    this->read_only = false;
    try {
      this->umap_region = Umap::umap_ex(0, this->region_size, this->PROT_RW, UMAP_PRIVATE, this->fd, 0, nullptr);
    } catch (const std::exception&) {
      this->umap_region = Umap::umap_ex(0, this->region_size, this->PROT_RO, UMAP_PRIVATE, this->fd, 0, nullptr);
      this->read_only = true;
    }
    if ( this->umap_region == UMAP_FAILED ) {
      throw TestException("umap failed");
    }
  }

  void init_region(uint64_t* const ptr, const uint64_t size, std::function<uint64_t(uint64_t)>& f) {
    for (uint64_t i = 0; i < size; i++) {
      ptr[i] = f(i);
    }
  }

public:
  umap_test(uint64_t region_size) : region_size(region_size) {
    this->fd = memfd_create("umap_test", 0);
    struct stat statbuf;
    if (::fstat(fd, &statbuf) == -1) {
      throw TestException("fstat failed: " + std::to_string(errno));
    }
    if (::fallocate(fd, 0, 0, region_size) == -1) {
      throw TestException("fallocate failed: " + std::to_string(errno));
    }
    this->do_umap();
    this->mmap_region = ::mmap(0, region_size, this->PROT_RW, MAP_SHARED | MAP_NORESERVE, fd, 0);
    if ( this->mmap_region == MAP_FAILED ) {
      throw TestException("mmap failed");
    }
  }

  ~umap_test() {
    close(this->fd);
    if (this->umap_region) { uunmap(this->umap_region, this->region_size); }
    if (this->mmap_region) { munmap(this->mmap_region, this->region_size); }
  }

  int run_test() {
    bool success = true;
    int rv;
    if (this->read_only) {
      std::cout << "Running read-only test" << std::endl;
    }
    uint64_t* const utest = static_cast<uint64_t*>(this->umap_region);
    uint64_t* const mtest = static_cast<uint64_t*>(this->mmap_region);
    const uint64_t len = this->region_size / sizeof(uint64_t);

    std::function<uint64_t(uint64_t)> seq = [](const uint64_t x)->uint64_t { return x; };
    std::function<uint64_t(uint64_t)> inv = [len](const uint64_t x)->uint64_t { return len-x; };

    // write test data
    if (this->read_only) {
      this->init_region(mtest, len, seq);
    } else {
      this->init_region(utest, len, seq);
    }

    // read test data
    for (uint64_t i = 0; i < this->region_size / sizeof(uint64_t); i++) {
      if (utest[i] != i) {
        success = false;
        break;
      }
    }

    if (success) {
      // run second pass
      if (this->read_only) {
        this->init_region(mtest, len, inv);
      } else {
        this->init_region(utest, len, inv);
      }

      for (uint64_t i = 0; i < this->region_size / sizeof(uint64_t); i++) {
        if (utest[i] != (len-i)) {
          success = false;
          break;
        }
      }
    }

    if (!success) {
      rv = umap_test::TEST_FAIL;
    } else if (success && read_only) {
      rv = umap_test::TEST_RO_PASS;
    } else {
      rv = umap_test::TEST_RW_PASS;
    }

    return rv;
  }
}; // class umap_test

} // namespace umaptest

int main() {
  const uint64_t umap_page_size = 128 * 1024ul;
  const uint64_t umap_buf_size = 64;
  const uint64_t num_pages = 256;
  int test_result = 0;
  int exit_status = -1;

  ::setenv("UMAP_BUFSIZE", std::to_string(umap_buf_size).c_str(), 1);
  ::setenv("UMAP_PAGESIZE", std::to_string(umap_page_size).c_str(), 1);

  try {
    umaptest::umap_test t(umap_page_size * num_pages);
    test_result = t.run_test();

    switch (test_result) {
      case umaptest::umap_test::TEST_RW_PASS:
        std::cout << "RW test passed." << std::endl;
        exit_status = 0;
        break;
      case umaptest::umap_test::TEST_RO_PASS:
        std::cout << "RO test passed." << std::endl;
        exit_status = 0;
        break;
      default:
        std::cout << "Test failed." << std::endl;
        exit_status = 1;
        break;
    }
  } catch (const std::exception&) {
    std::cout << "Test failed." << std::endl;
    exit_status = -1;
  }

  return exit_status;
}
