#!/bin/bash
echo "Script 6 starting....."
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src
/dev/shm/shea9/spack/lib/spack/env/gcc/gcc -O2  -std=c11 -Wall -DNDEBUG -DHAVE_SYMVER -D_LARGEFILE64_SOURCE=1 -DHAVE_POSIX_MEMALIGN -DHAVE_ALIGNED_ALLOC -DHAVE_SYS_AUXV_H -DZLIB_COMPAT -DWITH_GZFILEOP -DHAVE_VISIBILITY_HIDDEN -DHAVE_VISIBILITY_INTERNAL -DHAVE_ATTRIBUTE_ALIGNED -DHAVE_BUILTIN_CTZ -DHAVE_BUILTIN_CTZLL -DX86_FEATURES -DX86_AVX2 -DX86_AVX512 -DX86_MASK_INTRIN -DX86_AVX512VNNI -DX86_SSE42 -DX86_SSE2 -DX86_SSSE3 -DX86_PCLMULQDQ_CRC -DX86_VPCLMULQDQ_CRC -shared -Wl,-soname,libz.so.1,--version-script,/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/zlib.map  -o libz.so.1.3.0.zlib-ng  adler32.lo adler32_fold.lo chunkset.lo compare256.lo compress.lo cpu_features.lo crc32_braid.lo crc32_braid_comb.lo crc32_fold.lo deflate.lo deflate_fast.lo deflate_huff.lo deflate_medium.lo deflate_quick.lo deflate_rle.lo deflate_slow.lo deflate_stored.lo functable.lo infback.lo inflate.lo inftrees.lo insert_string.lo insert_string_roll.lo slide_hash.lo trees.lo uncompr.lo zutil.lo x86_features.lo slide_hash_avx2.lo chunkset_avx2.lo compare256_avx2.lo adler32_avx2.lo adler32_avx512.lo adler32_avx512_vnni.lo adler32_sse42.lo insert_string_sse42.lo chunkset_sse2.lo compare256_sse2.lo slide_hash_sse2.lo adler32_ssse3.lo chunkset_ssse3.lo crc32_pclmulqdq.lo crc32_vpclmulqdq.lo gzlib.lo gzread.lo gzwrite.lo 
echo "Script 6 done."
