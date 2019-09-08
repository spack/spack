/****************************/
/* THIS IS OPEN SOURCE CODE */
/****************************/

/* 
* File:    x86_cpuid_info.c
* Author:  Dan Terpstra
*          terpstra@eecs.utk.edu
*          complete rewrite of linux-memory.c to conform to latest docs
*          and convert Intel to a table driven implementation.
*          Now also supports multiple TLB descriptors
*/

#include <string.h>
#include <stdio.h>
#include "papi.h"
#include "papi_internal.h"

static void init_mem_hierarchy( PAPI_mh_info_t * mh_info );
static int init_amd( PAPI_mh_info_t * mh_info, int *levels );
static short int _amd_L2_L3_assoc( unsigned short int pattern );
static int init_intel( PAPI_mh_info_t * mh_info , int *levels);

#if defined( __amd64__ ) || defined (__x86_64__)
static inline void
cpuid( unsigned int *a, unsigned int *b, unsigned int *c, unsigned int *d )
{
	unsigned int op = *a;
	__asm__("cpuid;"
		: "=a" (*a), "=b" (*b), "=c" (*c), "=d" (*d)
		: "a" (op) );
}
#else
static inline void
cpuid( unsigned int *a, unsigned int *b, unsigned int *c, unsigned int *d )
{
	unsigned int op = *a;
	// .byte 0x53 == push ebx. it's universal for 32 and 64 bit
	// .byte 0x5b == pop ebx.
	// Some gcc's (4.1.2 on Core2) object to pairing push/pop and ebx in 64 bit mode.
	// Using the opcode directly avoids this problem.
  __asm__ __volatile__( ".byte 0x53\n\tcpuid\n\tmovl %%ebx, %%esi\n\t.byte 0x5b":"=a"( *a ), "=S"( *b ), "=c"( *c ),
						  "=d"
						  ( *d )
  :					  "a"( op ) );
}
#endif

int
_x86_cache_info( PAPI_mh_info_t * mh_info )
{
	int retval = 0;
	union
	{
		struct
		{
			unsigned int ax, bx, cx, dx;
		} e;
		char vendor[20];			   /* leave room for terminator bytes */
	} reg;

	/* Don't use cpu_type to determine the processor.
	 * get the information directly from the chip.
	 */
	reg.e.ax = 0;			 /* function code 0: vendor string */
	/* The vendor string is composed of EBX:EDX:ECX.
	 * by swapping the register addresses in the call below,
	 * the string is correctly composed in the char array.
	 */
	cpuid( &reg.e.ax, &reg.e.bx, &reg.e.dx, &reg.e.cx );
	reg.vendor[16] = 0;
	MEMDBG( "Vendor: %s\n", &reg.vendor[4] );

	init_mem_hierarchy( mh_info );

	if ( !strncmp( "GenuineIntel", &reg.vendor[4], 12 ) ) {
	        init_intel( mh_info, &mh_info->levels);
	} else if ( !strncmp( "AuthenticAMD", &reg.vendor[4], 12 ) ) {
	  init_amd( mh_info, &mh_info->levels );
	} else {
		MEMDBG( "Unsupported cpu type; Not Intel or AMD x86\n" );
		return PAPI_ENOIMPL;
	}

	/* This works only because an empty cache element is initialized to 0 */
	MEMDBG( "Detected L1: %d L2: %d  L3: %d\n",
			mh_info->level[0].cache[0].size + mh_info->level[0].cache[1].size,
			mh_info->level[1].cache[0].size + mh_info->level[1].cache[1].size,
			mh_info->level[2].cache[0].size + mh_info->level[2].cache[1].size );
	return retval;
}

static void
init_mem_hierarchy( PAPI_mh_info_t * mh_info )
{
	int i, j;
	PAPI_mh_level_t *L = mh_info->level;

	/* initialize entire memory hierarchy structure to benign values */
	for ( i = 0; i < PAPI_MAX_MEM_HIERARCHY_LEVELS; i++ ) {
		for ( j = 0; j < PAPI_MH_MAX_LEVELS; j++ ) {
			L[i].tlb[j].type = PAPI_MH_TYPE_EMPTY;
			L[i].tlb[j].num_entries = 0;
			L[i].tlb[j].associativity = 0;
			L[i].cache[j].type = PAPI_MH_TYPE_EMPTY;
			L[i].cache[j].size = 0;
			L[i].cache[j].line_size = 0;
			L[i].cache[j].num_lines = 0;
			L[i].cache[j].associativity = 0;
		}
	}
}

static short int
_amd_L2_L3_assoc( unsigned short int pattern )
{
	/* From "CPUID Specification" #25481 Rev 2.28, April 2008 */
	short int assoc[16] =
		{ 0, 1, 2, -1, 4, -1, 8, -1, 16, -1, 32, 48, 64, 96, 128, SHRT_MAX };
	if ( pattern > 0xF )
		return -1;
	return ( assoc[pattern] );
}

/* Cache configuration for AMD Athlon/Duron */
static int
init_amd( PAPI_mh_info_t * mh_info, int *num_levels )
{
	union
	{
		struct
		{
			unsigned int ax, bx, cx, dx;
		} e;
		unsigned char byt[16];
	} reg;
	int i, j, levels = 0;
	PAPI_mh_level_t *L = mh_info->level;

	/*
	 * Layout of CPU information taken from :
	 * "CPUID Specification" #25481 Rev 2.28, April 2008 for most current info.
	 */

	MEMDBG( "Initializing AMD memory info\n" );
	/* AMD level 1 cache info */
	reg.e.ax = 0x80000005;	 /* extended function code 5: L1 Cache and TLB Identifiers */
	cpuid( &reg.e.ax, &reg.e.bx, &reg.e.cx, &reg.e.dx );

	MEMDBG( "e.ax=%#8.8x e.bx=%#8.8x e.cx=%#8.8x e.dx=%#8.8x\n",
			reg.e.ax, reg.e.bx, reg.e.cx, reg.e.dx );
	MEMDBG
		( ":\neax: %#x %#x %#x %#x\nebx: %#x %#x %#x %#x\necx: %#x %#x %#x %#x\nedx: %#x %#x %#x %#x\n",
		  reg.byt[0], reg.byt[1], reg.byt[2], reg.byt[3], reg.byt[4],
		  reg.byt[5], reg.byt[6], reg.byt[7], reg.byt[8], reg.byt[9],
		  reg.byt[10], reg.byt[11], reg.byt[12], reg.byt[13], reg.byt[14],
		  reg.byt[15] );

	/* NOTE: We assume L1 cache and TLB always exists */
	/* L1 TLB info */

	/* 4MB memory page information; half the number of entries as 2MB */
	L[0].tlb[0].type = PAPI_MH_TYPE_INST;
	L[0].tlb[0].num_entries = reg.byt[0] / 2;
	L[0].tlb[0].page_size = 4096 << 10;
	L[0].tlb[0].associativity = reg.byt[1];

	L[0].tlb[1].type = PAPI_MH_TYPE_DATA;
	L[0].tlb[1].num_entries = reg.byt[2] / 2;
	L[0].tlb[1].page_size = 4096 << 10;
	L[0].tlb[1].associativity = reg.byt[3];

	/* 2MB memory page information */
	L[0].tlb[2].type = PAPI_MH_TYPE_INST;
	L[0].tlb[2].num_entries = reg.byt[0];
	L[0].tlb[2].page_size = 2048 << 10;
	L[0].tlb[2].associativity = reg.byt[1];

	L[0].tlb[3].type = PAPI_MH_TYPE_DATA;
	L[0].tlb[3].num_entries = reg.byt[2];
	L[0].tlb[3].page_size = 2048 << 10;
	L[0].tlb[3].associativity = reg.byt[3];

	/* 4k page information */
	L[0].tlb[4].type = PAPI_MH_TYPE_INST;
	L[0].tlb[4].num_entries = reg.byt[4];
	L[0].tlb[4].page_size = 4 << 10;
	L[0].tlb[4].associativity = reg.byt[5];

	L[0].tlb[5].type = PAPI_MH_TYPE_DATA;
	L[0].tlb[5].num_entries = reg.byt[6];
	L[0].tlb[5].page_size = 4 << 10;
	L[0].tlb[5].associativity = reg.byt[7];

	for ( i = 0; i < PAPI_MH_MAX_LEVELS; i++ ) {
		if ( L[0].tlb[i].associativity == 0xff )
			L[0].tlb[i].associativity = SHRT_MAX;
	}

	/* L1 D-cache info */
	L[0].cache[0].type =
		PAPI_MH_TYPE_DATA | PAPI_MH_TYPE_WB | PAPI_MH_TYPE_PSEUDO_LRU;
	L[0].cache[0].size = reg.byt[11] << 10;
	L[0].cache[0].associativity = reg.byt[10];
	L[0].cache[0].line_size = reg.byt[8];
	/* Byt[9] is "Lines per tag" */
	/* Is that == lines per cache? */
	/* L[0].cache[1].num_lines = reg.byt[9]; */
	if ( L[0].cache[0].line_size )
		L[0].cache[0].num_lines = L[0].cache[0].size / L[0].cache[0].line_size;
	MEMDBG( "D-Cache Line Count: %d; Computed: %d\n", reg.byt[9],
			L[0].cache[0].num_lines );

	/* L1 I-cache info */
	L[0].cache[1].type = PAPI_MH_TYPE_INST;
	L[0].cache[1].size = reg.byt[15] << 10;
	L[0].cache[1].associativity = reg.byt[14];
	L[0].cache[1].line_size = reg.byt[12];
	/* Byt[13] is "Lines per tag" */
	/* Is that == lines per cache? */
	/* L[0].cache[1].num_lines = reg.byt[13]; */
	if ( L[0].cache[1].line_size )
		L[0].cache[1].num_lines = L[0].cache[1].size / L[0].cache[1].line_size;
	MEMDBG( "I-Cache Line Count: %d; Computed: %d\n", reg.byt[13],
			L[0].cache[1].num_lines );

	for ( i = 0; i < 2; i++ ) {
		if ( L[0].cache[i].associativity == 0xff )
			L[0].cache[i].associativity = SHRT_MAX;
	}

	/* AMD L2/L3 Cache and L2 TLB info */
	/* NOTE: For safety we assume L2 and L3 cache and TLB may not exist */

	reg.e.ax = 0x80000006;	 /* extended function code 6: L2/L3 Cache and L2 TLB Identifiers */
	cpuid( &reg.e.ax, &reg.e.bx, &reg.e.cx, &reg.e.dx );

	MEMDBG( "e.ax=%#8.8x e.bx=%#8.8x e.cx=%#8.8x e.dx=%#8.8x\n",
			reg.e.ax, reg.e.bx, reg.e.cx, reg.e.dx );
	MEMDBG
		( ":\neax: %#x %#x %#x %#x\nebx: %#x %#x %#x %#x\necx: %#x %#x %#x %#x\nedx: %#x %#x %#x %#x\n",
		  reg.byt[0], reg.byt[1], reg.byt[2], reg.byt[3], reg.byt[4],
		  reg.byt[5], reg.byt[6], reg.byt[7], reg.byt[8], reg.byt[9],
		  reg.byt[10], reg.byt[11], reg.byt[12], reg.byt[13], reg.byt[14],
		  reg.byt[15] );

	/* L2 TLB info */

	if ( reg.byt[0] | reg.byt[1] ) {	/* Level 2 ITLB exists */
		/* 4MB ITLB page information; half the number of entries as 2MB */
		L[1].tlb[0].type = PAPI_MH_TYPE_INST;
		L[1].tlb[0].num_entries =
			( ( ( short ) ( reg.byt[1] & 0xF ) << 8 ) + reg.byt[0] ) / 2;
		L[1].tlb[0].page_size = 4096 << 10;
		L[1].tlb[0].associativity =
			_amd_L2_L3_assoc( ( reg.byt[1] & 0xF0 ) >> 4 );

		/* 2MB ITLB page information */
		L[1].tlb[2].type = PAPI_MH_TYPE_INST;
		L[1].tlb[2].num_entries = L[1].tlb[0].num_entries * 2;
		L[1].tlb[2].page_size = 2048 << 10;
		L[1].tlb[2].associativity = L[1].tlb[0].associativity;
	}

	if ( reg.byt[2] | reg.byt[3] ) {	/* Level 2 DTLB exists */
		/* 4MB DTLB page information; half the number of entries as 2MB */
		L[1].tlb[1].type = PAPI_MH_TYPE_DATA;
		L[1].tlb[1].num_entries =
			( ( ( short ) ( reg.byt[3] & 0xF ) << 8 ) + reg.byt[2] ) / 2;
		L[1].tlb[1].page_size = 4096 << 10;
		L[1].tlb[1].associativity =
			_amd_L2_L3_assoc( ( reg.byt[3] & 0xF0 ) >> 4 );

		/* 2MB DTLB page information */
		L[1].tlb[3].type = PAPI_MH_TYPE_DATA;
		L[1].tlb[3].num_entries = L[1].tlb[1].num_entries * 2;
		L[1].tlb[3].page_size = 2048 << 10;
		L[1].tlb[3].associativity = L[1].tlb[1].associativity;
	}

	/* 4k page information */
	if ( reg.byt[4] | reg.byt[5] ) {	/* Level 2 ITLB exists */
		L[1].tlb[4].type = PAPI_MH_TYPE_INST;
		L[1].tlb[4].num_entries =
			( ( short ) ( reg.byt[5] & 0xF ) << 8 ) + reg.byt[4];
		L[1].tlb[4].page_size = 4 << 10;
		L[1].tlb[4].associativity =
			_amd_L2_L3_assoc( ( reg.byt[5] & 0xF0 ) >> 4 );
	}
	if ( reg.byt[6] | reg.byt[7] ) {	/* Level 2 DTLB exists */
		L[1].tlb[5].type = PAPI_MH_TYPE_DATA;
		L[1].tlb[5].num_entries =
			( ( short ) ( reg.byt[7] & 0xF ) << 8 ) + reg.byt[6];
		L[1].tlb[5].page_size = 4 << 10;
		L[1].tlb[5].associativity =
			_amd_L2_L3_assoc( ( reg.byt[7] & 0xF0 ) >> 4 );
	}

	/* AMD Level 2 cache info */
	if ( reg.e.cx ) {
		L[1].cache[0].type =
			PAPI_MH_TYPE_UNIFIED | PAPI_MH_TYPE_WT | PAPI_MH_TYPE_PSEUDO_LRU;
		L[1].cache[0].size = ( int ) ( ( reg.e.cx & 0xffff0000 ) >> 6 );	/* right shift by 16; multiply by 2^10 */
		L[1].cache[0].associativity =
			_amd_L2_L3_assoc( ( reg.byt[9] & 0xF0 ) >> 4 );
		L[1].cache[0].line_size = reg.byt[8];
/*		L[1].cache[0].num_lines = reg.byt[9]&0xF; */
		if ( L[1].cache[0].line_size )
			L[1].cache[0].num_lines =
				L[1].cache[0].size / L[1].cache[0].line_size;
		MEMDBG( "U-Cache Line Count: %d; Computed: %d\n", reg.byt[9] & 0xF,
				L[1].cache[0].num_lines );
	}

	/* AMD Level 3 cache info (shared across cores) */
	if ( reg.e.dx ) {
		L[2].cache[0].type =
			PAPI_MH_TYPE_UNIFIED | PAPI_MH_TYPE_WT | PAPI_MH_TYPE_PSEUDO_LRU;
		L[2].cache[0].size = ( int ) ( reg.e.dx & 0xfffc0000 ) << 1;	/* in blocks of 512KB (2^19) */
		L[2].cache[0].associativity =
			_amd_L2_L3_assoc( ( reg.byt[13] & 0xF0 ) >> 4 );
		L[2].cache[0].line_size = reg.byt[12];
/*		L[2].cache[0].num_lines = reg.byt[13]&0xF; */
		if ( L[2].cache[0].line_size )
			L[2].cache[0].num_lines =
				L[2].cache[0].size / L[2].cache[0].line_size;
		MEMDBG( "U-Cache Line Count: %d; Computed: %d\n", reg.byt[13] & 0xF,
				L[1].cache[0].num_lines );
	}
	for ( i = 0; i < PAPI_MAX_MEM_HIERARCHY_LEVELS; i++ ) {
		for ( j = 0; j < PAPI_MH_MAX_LEVELS; j++ ) {
			/* Compute the number of levels of hierarchy actually used */
			if ( L[i].tlb[j].type != PAPI_MH_TYPE_EMPTY ||
				 L[i].cache[j].type != PAPI_MH_TYPE_EMPTY )
				levels = i + 1;
		}
	}
	*num_levels = levels;
	return PAPI_OK;
}

   /*
    * The data from this table now comes from figure 3-17 in
    *  the Intel Architectures Software Reference Manual 2A
    *  (cpuid instruction section)
    * 
    * Pretviously the information was provided by
    * "Intel® Processor Identification and the CPUID Instruction",
    * Application Note, AP-485, Nov 2008, 241618-033
    * Updated to AP-485, Aug 2009, 241618-036
    *
    * The following data structure and its instantiation trys to
    * capture all the information in Section 2.1.3 of the above
    * document. Not all of it is used by PAPI, but it could be.
    * As the above document is revised, this table should be
    * updated.
    */

#define TLB_SIZES 3			 /* number of different page sizes for a single TLB descriptor */
struct _intel_cache_info
{
	int descriptor;					   /* 0x00 - 0xFF: register descriptor code */
	int level;						   /* 1 to PAPI_MH_MAX_LEVELS */
	int type;						   /* Empty, instr, data, vector, unified | TLB */
	int size[TLB_SIZES];			   /* cache or  TLB page size(s) in kB */
	int associativity;				   /* SHRT_MAX == fully associative */
	int sector;						   /* 1 if cache is sectored; else 0 */
	int line_size;					   /* for cache */
	int entries;					   /* for TLB */
};

static struct _intel_cache_info intel_cache[] = {
// 0x01
	{.descriptor = 0x01,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 32,
	 },
// 0x02
	{.descriptor = 0x02,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size[0] = 4096,
	 .associativity = SHRT_MAX,
	 .entries = 2,
	 },
// 0x03
	{.descriptor = 0x03,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 64,
	 },
// 0x04
	{.descriptor = 0x04,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4096,
	 .associativity = 4,
	 .entries = 8,
	 },
// 0x05
	{.descriptor = 0x05,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4096,
	 .associativity = 4,
	 .entries = 32,
	 },
// 0x06
	{.descriptor = 0x06,
	 .level = 1,
	 .type = PAPI_MH_TYPE_INST,
	 .size[0] = 8,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x08
	{.descriptor = 0x08,
	 .level = 1,
	 .type = PAPI_MH_TYPE_INST,
	 .size[0] = 16,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x09
	{.descriptor = 0x09,
	 .level = 1,
	 .type = PAPI_MH_TYPE_INST,
	 .size[0] = 32,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0x0A
	{.descriptor = 0x0A,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 8,
	 .associativity = 2,
	 .line_size = 32,
	 },
// 0x0B
	{.descriptor = 0x0B,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size[0] = 4096,
	 .associativity = 4,
	 .entries = 4,
	 },   
// 0x0C
	{.descriptor = 0x0C,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 16,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x0D
	{.descriptor = 0x0D,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 16,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0x0E
	{.descriptor = 0x0E,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 24,
	 .associativity = 6,
	 .line_size = 64,
	 },   
// 0x21
	{.descriptor = 0x21,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 256,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0x22
	{.descriptor = 0x22,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 4,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x23
	{.descriptor = 0x23,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x25
	{.descriptor = 0x25,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 2048,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x29
	{.descriptor = 0x29,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 4096,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x2C
	{.descriptor = 0x2C,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 32,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0x30
	{.descriptor = 0x30,
	 .level = 1,
	 .type = PAPI_MH_TYPE_INST,
	 .size[0] = 32,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0x39
	{.descriptor = 0x39,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 128,
	 .associativity = 4,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x3A
	{.descriptor = 0x3A,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 192,
	 .associativity = 6,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x3B
	{.descriptor = 0x3B,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 128,
	 .associativity = 2,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x3C
	{.descriptor = 0x3C,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 256,
	 .associativity = 4,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x3D
	{.descriptor = 0x3D,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 384,
	 .associativity = 6,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x3E
	{.descriptor = 0x3E,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 4,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x40: no last level cache (??)
// 0x41
	{.descriptor = 0x41,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 128,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x42
	{.descriptor = 0x42,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 256,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x43
	{.descriptor = 0x43,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x44
	{.descriptor = 0x44,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x45
	{.descriptor = 0x45,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 2048,
	 .associativity = 4,
	 .line_size = 32,
	 },
// 0x46
	{.descriptor = 0x46,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 4096,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0x47
	{.descriptor = 0x47,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 8192,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0x48
	{.descriptor = 0x48,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 3072,
	 .associativity = 12,
	 .line_size = 64,
	 },
// 0x49 NOTE: for family 0x0F model 0x06 this is level 3
	{.descriptor = 0x49,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 4096,
	 .associativity = 16,
	 .line_size = 64,
	 },
// 0x4A
	{.descriptor = 0x4A,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 6144,
	 .associativity = 12,
	 .line_size = 64,
	 },
// 0x4B
	{.descriptor = 0x4B,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 8192,
	 .associativity = 16,
	 .line_size = 64,
	 },
// 0x4C
	{.descriptor = 0x4C,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 12288,
	 .associativity = 12,
	 .line_size = 64,
	 },
// 0x4D
	{.descriptor = 0x4D,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 16384,
	 .associativity = 16,
	 .line_size = 64,
	 },
// 0x4E
	{.descriptor = 0x4E,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 6144,
	 .associativity = 24,
	 .line_size = 64,
	 },
// 0x4F
	{.descriptor = 0x4F,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size[0] = 4,
	 .associativity = SHRT_MAX,
	 .entries = 32,
	 },
// 0x50
	{.descriptor = 0x50,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size = {4, 2048, 4096},
	 .associativity = SHRT_MAX,
	 .entries = 64,
	 },
// 0x51
	{.descriptor = 0x51,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size = {4, 2048, 4096},
	 .associativity = SHRT_MAX,
	 .entries = 128,
	 },
// 0x52
	{.descriptor = 0x52,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size = {4, 2048, 4096},
	 .associativity = SHRT_MAX,
	 .entries = 256,
	 },
// 0x55
	{.descriptor = 0x55,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size = {2048, 4096, 0},
	 .associativity = SHRT_MAX,
	 .entries = 7,
	 },
// 0x56
	{.descriptor = 0x56,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4096,
	 .associativity = 4,
	 .entries = 16,
	 },
// 0x57
	{.descriptor = 0x57,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 16,
	 },
// 0x59
	{.descriptor = 0x59,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4,
	 .associativity = SHRT_MAX,
	 .entries = 16,
	 },   
// 0x5A
	{.descriptor = 0x5A,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size = {2048, 4096, 0},
	 .associativity = 4,
	 .entries = 32,
	 },
// 0x5B
	{.descriptor = 0x5B,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size = {4, 4096, 0},
	 .associativity = SHRT_MAX,
	 .entries = 64,
	 },
// 0x5C
	{.descriptor = 0x5C,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size = {4, 4096, 0},
	 .associativity = SHRT_MAX,
	 .entries = 128,
	 },
// 0x5D
	{.descriptor = 0x5D,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size = {4, 4096, 0},
	 .associativity = SHRT_MAX,
	 .entries = 256,
	 },
// 0x60
	{.descriptor = 0x60,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 16,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x66
	{.descriptor = 0x66,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 8,
	 .associativity = 4,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x67
	{.descriptor = 0x67,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 16,
	 .associativity = 4,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x68
	{.descriptor = 0x68,
	 .level = 1,
	 .type = PAPI_MH_TYPE_DATA,
	 .size[0] = 32,
	 .associativity = 4,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x70
	{.descriptor = 0x70,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TRACE,
	 .size[0] = 12,
	 .associativity = 8,
	 },
// 0x71
	{.descriptor = 0x71,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TRACE,
	 .size[0] = 16,
	 .associativity = 8,
	 },
// 0x72
	{.descriptor = 0x72,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TRACE,
	 .size[0] = 32,
	 .associativity = 8,
	 },
// 0x73
	{.descriptor = 0x73,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TRACE,
	 .size[0] = 64,
	 .associativity = 8,
	 },
// 0x78
	{.descriptor = 0x78,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0x79
	{.descriptor = 0x79,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 128,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x7A
	{.descriptor = 0x7A,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 256,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x7B
	{.descriptor = 0x7B,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x7C
	{.descriptor = 0x7C,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 8,
	 .sector = 1,
	 .line_size = 64,
	 },
// 0x7D
	{.descriptor = 0x7D,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 2048,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0x7F
	{.descriptor = 0x7F,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 2,
	 .line_size = 64,
	 },
// 0x80
	{.descriptor = 0x80,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 8,
	 .line_size = 64,
	 },   
// 0x82
	{.descriptor = 0x82,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 256,
	 .associativity = 8,
	 .line_size = 32,
	 },
// 0x83
	{.descriptor = 0x83,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 8,
	 .line_size = 32,
	 },
// 0x84
	{.descriptor = 0x84,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 8,
	 .line_size = 32,
	 },
// 0x85
	{.descriptor = 0x85,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 2048,
	 .associativity = 8,
	 .line_size = 32,
	 },
// 0x86
	{.descriptor = 0x86,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0x87
	{.descriptor = 0x87,
	 .level = 2,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0xB0
	{.descriptor = 0xB0,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 128,
	 },
// 0xB1 NOTE: This is currently the only instance where .entries
//      is dependent on .size. It's handled as a code exception.
//      If other instances appear in the future, the structure
//      should probably change to accomodate it.
	{.descriptor = 0xB1,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size = {2048, 4096, 0},
	 .associativity = 4,
	 .entries = 8,			 /* or 4 if size = 4096 */
	 },
// 0xB2
	{.descriptor = 0xB2,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_INST,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 64,
	 },
// 0xB3
	{.descriptor = 0xB3,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 128,
	 },
// 0xB4
	{.descriptor = 0xB4,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 256,
	 },
// 0xBA
	{.descriptor = 0xBA,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 64,
	 },   
// 0xC0
	{.descriptor = 0xBA,
	 .level = 1,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_DATA,
	 .size = {4,4096},
	 .associativity = 4,
	 .entries = 8,
	 },      
// 0xCA
	{.descriptor = 0xCA,
	 .level = 2,
	 .type = PAPI_MH_TYPE_TLB | PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 4,
	 .associativity = 4,
	 .entries = 512,
	 },
// 0xD0
	{.descriptor = 0xD0,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 512,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0xD1
	{.descriptor = 0xD1,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0xD2
	{.descriptor = 0xD2,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 2048,
	 .associativity = 4,
	 .line_size = 64,
	 },
// 0xD6
	{.descriptor = 0xD6,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1024,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0xD7
	{.descriptor = 0xD7,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 2048,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0xD8
	{.descriptor = 0xD8,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 4096,
	 .associativity = 8,
	 .line_size = 64,
	 },
// 0xDC
	{.descriptor = 0xDC,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 1536,
	 .associativity = 12,
	 .line_size = 64,
	 },
// 0xDD
	{.descriptor = 0xDD,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 3072,
	 .associativity = 12,
	 .line_size = 64,
	 },
// 0xDE
	{.descriptor = 0xDE,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 6144,
	 .associativity = 12,
	 .line_size = 64,
	 },
// 0xE2
	{.descriptor = 0xE2,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 2048,
	 .associativity = 16,
	 .line_size = 64,
	 },
// 0xE3
	{.descriptor = 0xE3,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 4096,
	 .associativity = 16,
	 .line_size = 64,
	 },
// 0xE4
	{.descriptor = 0xE4,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 8192,
	 .associativity = 16,
	 .line_size = 64,
	 },
// 0xEA
	{.descriptor = 0xEA,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 12288,
	 .associativity = 24,
	 .line_size = 64,
	 },
// 0xEB
	{.descriptor = 0xEB,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 18432,
	 .associativity = 24,
	 .line_size = 64,
	 },
// 0xEC
	{.descriptor = 0xEC,
	 .level = 3,
	 .type = PAPI_MH_TYPE_UNIFIED,
	 .size[0] = 24576,
	 .associativity = 24,
	 .line_size = 64,
	 },
// 0xF0
	{.descriptor = 0xF0,
	 .level = 1,
	 .type = PAPI_MH_TYPE_PREF,
	 .size[0] = 64,
	 },
// 0xF1
	{.descriptor = 0xF1,
	 .level = 1,
	 .type = PAPI_MH_TYPE_PREF,
	 .size[0] = 128,
	 },
};

#ifdef DEBUG
static void
print_intel_cache_table(  )
{
	int i, j, k =
		( int ) ( sizeof ( intel_cache ) /
				  sizeof ( struct _intel_cache_info ) );
	for ( i = 0; i < k; i++ ) {
		printf( "%d.\tDescriptor: %#x\n", i, intel_cache[i].descriptor );
		printf( "\t  Level:     %d\n", intel_cache[i].level );
		printf( "\t  Type:      %d\n", intel_cache[i].type );
		printf( "\t  Size(s):   " );
		for ( j = 0; j < TLB_SIZES; j++ )
			printf( "%d, ", intel_cache[i].size[j] );
		printf( "\n" );
		printf( "\t  Assoc:     %d\n", intel_cache[i].associativity );
		printf( "\t  Sector:    %d\n", intel_cache[i].sector );
		printf( "\t  Line Size: %d\n", intel_cache[i].line_size );
		printf( "\t  Entries:   %d\n", intel_cache[i].entries );
		printf( "\n" );
	}
}
#endif

/* Given a specific cache descriptor, this routine decodes the information from a table
 * of such descriptors and fills out one or more records in a PAPI data structure.
 * Called only by init_intel()
 */
static void
intel_decode_descriptor( struct _intel_cache_info *d, PAPI_mh_level_t * L )
{
	int i, next;
	int level = d->level - 1;
	PAPI_mh_tlb_info_t *t;
	PAPI_mh_cache_info_t *c;

	if ( d->descriptor == 0x49 ) {	/* special case */
		unsigned int r_eax, r_ebx, r_ecx, r_edx;
		r_eax = 0x1;		 /* function code 1: family & model */
		cpuid( &r_eax, &r_ebx, &r_ecx, &r_edx );
		/* override table for Family F, model 6 only */
		if ( ( r_eax & 0x0FFF3FF0 ) == 0xF60 )
			level = 3;
	}
	if ( d->type & PAPI_MH_TYPE_TLB ) {
		for ( next = 0; next < PAPI_MH_MAX_LEVELS - 1; next++ ) {
			if ( L[level].tlb[next].type == PAPI_MH_TYPE_EMPTY )
				break;
		}
		/* expand TLB entries for multiple possible page sizes */
		for ( i = 0; i < TLB_SIZES && next < PAPI_MH_MAX_LEVELS && d->size[i];
			  i++, next++ ) {
//          printf("Level %d Descriptor: %#x TLB type %#x next: %d, i: %d\n", level, d->descriptor, d->type, next, i);
			t = &L[level].tlb[next];
			t->type = PAPI_MH_CACHE_TYPE( d->type );
			t->num_entries = d->entries;
			t->page_size = d->size[i] << 10;	/* minimum page size in KB */
			t->associativity = d->associativity;
			/* another special case */
			if ( d->descriptor == 0xB1 && d->size[i] == 4096 )
				t->num_entries = d->entries / 2;
		}
	} else {
		for ( next = 0; next < PAPI_MH_MAX_LEVELS - 1; next++ ) {
			if ( L[level].cache[next].type == PAPI_MH_TYPE_EMPTY )
				break;
		}
//      printf("Level %d Descriptor: %#x Cache type %#x next: %d\n", level, d->descriptor, d->type, next);
		c = &L[level].cache[next];
		c->type = PAPI_MH_CACHE_TYPE( d->type );
		c->size = d->size[0] << 10;	/* convert from KB to bytes */
		c->associativity = d->associativity;
		if ( d->line_size ) {
			c->line_size = d->line_size;
			c->num_lines = c->size / c->line_size;
		}
	}
}

#if defined(__amd64__) || defined(__x86_64__)
static inline void
cpuid2( unsigned int*eax, unsigned int* ebx,
		unsigned int*ecx, unsigned int *edx,
		unsigned int index, unsigned int ecx_in )
{
	__asm__ __volatile__ ("cpuid;"
		: "=a" (*eax), "=b" (*ebx), "=c" (*ecx), "=d" (*edx)
		: "0" (index), "2"(ecx_in) );
}
#else
static inline void
cpuid2 ( unsigned int* eax, unsigned int* ebx, 
                    unsigned int* ecx, unsigned int* edx, 
                    unsigned int index, unsigned int ecx_in )
{
  unsigned int a,b,c,d;
  __asm__ __volatile__ (".byte 0x53\n\tcpuid\n\tmovl %%ebx, %%esi\n\t.byte 0x5b"
		: "=a" (a), "=S" (b), "=c" (c), "=d" (d) \
		: "0" (index), "2"(ecx_in) );
  *eax = a; *ebx = b; *ecx = c; *edx = d;
}
#endif


static int
init_intel_leaf4( PAPI_mh_info_t * mh_info, int *num_levels )
{

  unsigned int eax, ebx, ecx, edx;
  unsigned int maxidx, ecx_in;
  int next;

  int cache_type,cache_level,cache_selfinit,cache_fullyassoc;
  int cache_linesize,cache_partitions,cache_ways,cache_sets;

  PAPI_mh_cache_info_t *c;

  *num_levels=0;

  cpuid2(&eax,&ebx,&ecx,&edx, 0, 0);
  maxidx = eax;
  
  if (maxidx<4) {
    MEMDBG("Warning!  CPUID Index 4 not supported!\n");
    return PAPI_ENOSUPP;
  }

  ecx_in=0;
  while(1) {
    cpuid2(&eax,&ebx,&ecx,&edx, 4, ecx_in);


    
    /* decoded as per table 3-12 in Intel Software Developer's Manual Volume 2A */
     
    cache_type=eax&0x1f;
    if (cache_type==0) break;     
     
    cache_level=(eax>>5)&0x3;
    cache_selfinit=(eax>>8)&0x1;
    cache_fullyassoc=(eax>>9)&0x1;

    cache_linesize=(ebx&0xfff)+1;
    cache_partitions=((ebx>>12)&0x3ff)+1;
    cache_ways=((ebx>>22)&0x3ff)+1;
       
    cache_sets=(ecx)+1;

    /* should we export this info?

    cache_maxshare=((eax>>14)&0xfff)+1;
    cache_maxpackage=((eax>>26)&0x3f)+1;
     
    cache_wb=(edx)&1;
    cache_inclusive=(edx>>1)&1;
    cache_indexing=(edx>>2)&1;
    */

    if (cache_level>*num_levels) *num_levels=cache_level;

    /* find next slot available to hold cache info */
    for ( next = 0; next < PAPI_MH_MAX_LEVELS - 1; next++ ) {
        if ( mh_info->level[cache_level-1].cache[next].type == PAPI_MH_TYPE_EMPTY ) break;
    }

    c=&(mh_info->level[cache_level-1].cache[next]);

    switch(cache_type) {
      case 1: MEMDBG("L%d Data Cache\n",cache_level); 
	c->type=PAPI_MH_TYPE_DATA;
	break;
      case 2: MEMDBG("L%d Instruction Cache\n",cache_level); 
	c->type=PAPI_MH_TYPE_INST;
	break;
      case 3: MEMDBG("L%d Unified Cache\n",cache_level); 
	c->type=PAPI_MH_TYPE_UNIFIED;
	break;
    }
     
    if (cache_selfinit) { MEMDBG("\tSelf-init\n"); }
    if (cache_fullyassoc) { MEMDBG("\tFully Associtative\n"); }
     
    //MEMDBG("\tMax logical processors sharing cache: %d\n",cache_maxshare);
    //MEMDBG("\tMax logical processors sharing package: %d\n",cache_maxpackage);
     
    MEMDBG("\tCache linesize: %d\n",cache_linesize);

    MEMDBG("\tCache partitions: %d\n",cache_partitions);
    MEMDBG("\tCache associaticity: %d\n",cache_ways);

    MEMDBG("\tCache sets: %d\n",cache_sets);
    MEMDBG("\tCache size = %dkB\n",
	   (cache_ways*cache_partitions*cache_linesize*cache_sets)/1024);

    //MEMDBG("\tWBINVD/INVD acts on lower caches: %d\n",cache_wb);
    //MEMDBG("\tCache is not inclusive: %d\n",cache_inclusive);
    //MEMDBG("\tComplex cache indexing: %d\n",cache_indexing);

    c->line_size=cache_linesize;
    if (cache_fullyassoc) {
       c->associativity=SHRT_MAX;
    }
    else {
       c->associativity=cache_ways;
    }
    c->size=(cache_ways*cache_partitions*cache_linesize*cache_sets);
    c->num_lines=cache_ways*cache_partitions*cache_sets;
     
    ecx_in++;
  }
  return PAPI_OK;
}

static int
init_intel_leaf2( PAPI_mh_info_t * mh_info , int *num_levels)
{
	/* cpuid() returns memory copies of 4 32-bit registers
	 * this union allows them to be accessed as either registers
	 * or individual bytes. Remember that Intel is little-endian.
	 */
	union
	{
		struct
		{
			unsigned int ax, bx, cx, dx;
		} e;
		unsigned char descrip[16];
	} reg;

	int r;							   /* register boundary index */
	int b;							   /* byte index into a register */
	int i;							   /* byte index into the descrip array */
	int t;							   /* table index into the static descriptor table */
	int count;						   /* how many times to call cpuid; from eax:lsb */
	int size;						   /* size of the descriptor table */
	int last_level = 0;				   /* how many levels in the cache hierarchy */

	/* All of Intel's cache info is in 1 call to cpuid
	 * however it is a table lookup :(
	 */
	MEMDBG( "Initializing Intel Cache and TLB descriptors\n" );

#ifdef DEBUG
	if ( ISLEVEL( DEBUG_MEMORY ) )
		print_intel_cache_table(  );
#endif

	reg.e.ax = 0x2;			 /* function code 2: cache descriptors */
	cpuid( &reg.e.ax, &reg.e.bx, &reg.e.cx, &reg.e.dx );

	MEMDBG( "e.ax=%#8.8x e.bx=%#8.8x e.cx=%#8.8x e.dx=%#8.8x\n",
			reg.e.ax, reg.e.bx, reg.e.cx, reg.e.dx );
	MEMDBG
		( ":\nd0: %#x %#x %#x %#x\nd1: %#x %#x %#x %#x\nd2: %#x %#x %#x %#x\nd3: %#x %#x %#x %#x\n",
		  reg.descrip[0], reg.descrip[1], reg.descrip[2], reg.descrip[3],
		  reg.descrip[4], reg.descrip[5], reg.descrip[6], reg.descrip[7],
		  reg.descrip[8], reg.descrip[9], reg.descrip[10], reg.descrip[11],
		  reg.descrip[12], reg.descrip[13], reg.descrip[14], reg.descrip[15] );

	count = reg.descrip[0];	 /* # times to repeat CPUID call. Not implemented. */

	/* Knights Corner at least returns 0 here */
	if (count==0) goto early_exit;

	size = ( sizeof ( intel_cache ) / sizeof ( struct _intel_cache_info ) );	/* # descriptors */
	MEMDBG( "Repeat cpuid(2,...) %d times. If not 1, code is broken.\n",
			count );
	if (count!=1) {
	   fprintf(stderr,"Warning: Unhandled cpuid count of %d\n",count);
	}

	for ( r = 0; r < 4; r++ ) {	/* walk the registers */
		if ( ( reg.descrip[r * 4 + 3] & 0x80 ) == 0 ) {	/* only process if high order bit is 0 */
			for ( b = 3; b >= 0; b-- ) {	/* walk the descriptor bytes from high to low */
				i = r * 4 + b;	/* calculate an index into the array of descriptors */
				if ( i ) {	 /* skip the low order byte in eax [0]; it's the count (see above) */
				   if ( reg.descrip[i] == 0xff ) {
				      MEMDBG("Warning! PAPI x86_cache: must implement cpuid leaf 4\n");
				      return PAPI_ENOSUPP;
				      /* we might continue instead */
				      /* in order to get TLB info  */
				      /* continue;                 */
				   }
					for ( t = 0; t < size; t++ ) {	/* walk the descriptor table */					   
						if ( reg.descrip[i] == intel_cache[t].descriptor ) {	/* find match */
							if ( intel_cache[t].level > last_level )
								last_level = intel_cache[t].level;
							intel_decode_descriptor( &intel_cache[t],
													 mh_info->level );
						}
					}
				}
			}
		}
	}
early_exit:
	MEMDBG( "# of Levels: %d\n", last_level );
	*num_levels=last_level;
	return PAPI_OK;
}


static int
init_intel( PAPI_mh_info_t * mh_info, int *levels )
{

  int result;
  int num_levels;

  /* try using the oldest leaf2 method first */
  result=init_intel_leaf2(mh_info, &num_levels);
  
  if (result!=PAPI_OK) {
     /* All Core2 and newer also support leaf4 detection */
     /* Starting with Westmere *only* leaf4 is supported */
     result=init_intel_leaf4(mh_info, &num_levels);
  }

  *levels=num_levels;
  return PAPI_OK;
}


/* Returns 1 if hypervisor detected */
/* Returns 0 if none found.         */
int 
_x86_detect_hypervisor(char *vendor_name)
{
  unsigned int eax, ebx, ecx, edx;
  char hyper_vendor_id[13];

  cpuid2(&eax, &ebx, &ecx, &edx,0x1,0);
  /* This is the hypervisor bit, ecx bit 31 */
  if  (ecx&0x80000000) {
    /* There are various values in the 0x4000000X range */
    /* It is questionable how standard they are         */
    /* For now we just return the name.                 */
    cpuid2(&eax, &ebx, &ecx, &edx, 0x40000000,0);
    memcpy(hyper_vendor_id + 0, &ebx, 4);
    memcpy(hyper_vendor_id + 4, &ecx, 4);
    memcpy(hyper_vendor_id + 8, &edx, 4);
    hyper_vendor_id[12] = '\0';
    strncpy(vendor_name,hyper_vendor_id,PAPI_MAX_STR_LEN);
    return 1;
  }
  else {
    strncpy(vendor_name,"none",PAPI_MAX_STR_LEN);
  }
  return 0;
}
