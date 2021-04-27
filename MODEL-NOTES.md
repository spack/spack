# Type / Location Model Notes

This is what I'm currently doing. Please yell at me if something is wrong!
There are a lot of details and I want to get them down here so you can also
look them over carefully and give feedback. You can also just look at the modified
asp.py in the pull request for the "code documentation" version. :)

## 1. Defining Interfaces

We define subprograms (functions) as interfaces. 

Interfaces
 - DW_TAG_subprogram (function)

I'll add other interfaces to this but want to make sure I'm doing functions correctly first.

## 2. Defining DIEs we want to parse

Of all the DW_TAG_*s, I'm currently parsing:

Parsing
 - **all interfaces noted above**
 - DW_TAG_formal_parameter
 - DW_TAG_variable (don't have predictible parents, we skip DW_AT_declaration)
 - DW_TAG_pointer_type/DW_TAG_pointer (not sure the latter exists)
 - DW_TAG_variable

Given the above, we sometimes hit children that we explicitly don't want to parse.
So I'm currently skipping:

 - DW_TAG_subroutine_type

because I'm not sure how to parse it. More specifically, we hit formal_parameters with
a parent that is a subroutine type. Since I can't represent this easily with name, I
skip over it.

## 3. Relationships?

I am currently skipping adding relationships for has_child because I'm
hoping to represent the relationship as flat (e.g., the name of a function
and variable in the same fact). However this might get complicated if we have functions
and/or variables with the same name within a corpus. In this case we need to go back to
giving each a unique id based on its name, parent, and corpus. I 
do a check early on based on the die "abbreviation code" in the scope of a corpus
to make sure we don't parse any DIEs twice. 

## 4. Base of Model is Name, Type, Location

My basic approach is to try and represent every DIE as a name, location, and die type.

```python
# We want to represent things as names, locations, and types
name = None
loc = None
die_type = None
```

### Find a name

I first look for a name, which can be the `DW_AT_linkage_name` (the mangled string)
or a `DW_AT_name`. 

### If it's an interface, atomize it

If we find a name and the tag is a known interface, I define it as such.
I skip and keep going if there is not a name. I'm not sure how to define an interface that doesn't have one, or even what that means.

```python
# We can only declare an interface with a name
if tag in interfaces and name:
    self.gen.fact(fn.interface(corpus.basename, name))     
elif tag in interfaces and not name:
    return
```

### Skip things that cannot be named

In testing I found that all libraries typically have a pointer type that is empty.
I think maybe it's just for declaring the size of a pointer? I skip over these
because there is basically no metadata that we need. It's not a named thing.

```python
# There can be a mostly empty pointer type that just states the size
# of a pointer in bytes, with the only parent being the compile unit
if not name and tag == "pointer_type":
    return
```

But I suspect if two libraries have different size pointer types, that's kind of weird
and would be an issue. But it's not in scope for our current modeling attempt so I'm skipping it.

If I've found a variable tag and it does not have a name, I also don't know how
to parse that so I skip it. In testing some of these have `DW_AT_specification`
which I suspect is some kind of reference? Possibly we could follow the reference
to get a name?

```python
# This has DW_AT_specification (a reference?) but no name, not sure
# how to handle
elif not name and tag == "variable":
    return
```

Matt mentioned that we would want to parse pointers something like:

```python
abi_typelocation('exe', 'main', 'char**', 'fb-32')
```

But in testing I haven't hit one yet - it's more likely to be hit when
I am deriving a type for another DIE (next section). For the DIEs that we loop over, this case has not triggered

```python
if "pointer" in tag:
    print('pointer')
    import IPython
    IPython.embed()
```

### Get the die type and name

Once we get over the "special cases" humps above, we can usually try to get
a  location and type.

```python
# DW_AT_type is a reference to another die (the type)
if "DW_AT_type" in die.attributes:
    die_type = self._get_die_type(die)

if "DW_AT_location" in die.attributes:
    loc = self.get_location(die)
```

This (I think) is done fairly reasonably - I was hitting an error where an
address was outside of a CU unit, but I read that I just need to add the CU offset
(and then I get an answer). 

```python
# DWARFError: refaddr 48991 not in DIE range of CU 66699
# https://github.com/eliben/pyelftools/blob/master/elftools/dwarf/compileunit.py#L113
# When using a reference class attribute with a form that is
# relative to the compile unit, add unit add the compile unit's
# .cu_addr before calling this function.
except et.exceptions.DWARFError:
    type_die = query_die.cu.get_DIE_from_refaddr(
    query_die.attributes["DW_AT_type"].value + query_die.cu.cu_offset
)
```

In my dummy case I haven't yet seen any `DW_AT_type` that have a ref address
which means an absolute offset.

```python
# Absolute offset
elif query_die.attributes["DW_AT_type"].startswith("DW_FORM_ref_addr")
```

Given that we have a type_die (derived from an address we either need to):

1. recursively call the function if that thing still has a `DW_AT_type` attribute
2. If the type_die tag is `DW_TAG_const_type` I return "const" as the string of the type
3. same with structure or pointer for `DW_TAG_structure_type` and `DW_TAG_pointer_type`
4. otherwise I get the type name again from `DW_AT_linkage_type` or `DW_AT_name`.


Note that I'm using cu.cu_offset instead of cu.cu_die_offset (which from the
comments above I think is the one I want?)

## 5. Variables with locations can be atomized

In testing they don't appear to have any kind of useful parent (e.g.,
a formal parameter would have a function parent). So we just parse them
into atoms and include their name, type, and location.

```python
# Variables don't necessarily have a parent function
if "variable" in tag and loc:
    fact = fn.abi_typelocation(corpus.basename, name, die_type, loc)
    self.gen.fact(fact)
    return
```
I don't check if there is a defined die_type - this could currently show
up with die_type as none.

## 6. Atomize function return type

Matt told me that if we have a function (subprogram) with a type,
the type is the return type! Huzzah! In practice I don't see that
these have any locations, but I also am no longer checking.

```
# If it's a subprogram and we have a type, it's a return type!
# abi_typelocation('exe', 'main', 'int', 'return')
if tag == "function" and die_type:
     cname = corpus.basename
     parent = os.path.basename(
         self.bytes2str(die.get_parent().attributes['DW_AT_name'].value)
     )
     fact = fn.abi_typelocation(cname, parent, name, die_type, "return")
     self.gen.fact(fact)            
     return
```

## 7. Functions without return types

Functions without types means that there is no return, so we exit because
we've already declared it to be an interface and don't need to parse the die
further (the children will be parsed later).

```python
elif tag == "function" and not die_type:
    return
```
I don't check if a function without a type has a location. From the examples
I saw, we weren't representing functions as having locations, but rather their
parameters.

## 8. Bail out on DW_AT_declaration

This is what I read is a "non complete type" and in testing I didn't see
that there was enough metadata to make a full atom, so we bail out.

```python
# Not sure how to parse non complete types (skip for now)
# https://stackoverflow.com/questions/38225269/dwarf-reading-not-complete-types
elif "DW_AT_declaration" in die.attributes:
    return
```

## 9. Atomize formal parameters

At this point I always do a sanity check (since we are still developing that
there is both a location AND die type. Since we are just parsing functions,
this is where we are defining atoms for formal paramters. If the parent is a subprogram
I add it to the atom, otherwise I try to define a general type/location for whatever
I've found (typically a variable)

```python
# We need to link the name of the (usually parameter) to its 
# parent function name
parent = die.get_parent()

# Variables might not have a parent
if "subprogram" not in parent.tag:
    fact = fn.abi_typelocation(corpus.basename, name, die_type, loc)
else:
    pname = self.bytes2str(parent.attributes['DW_AT_name'].value)
    fact = fn.abi_typelocation(corpus.basename, pname, name, die_type, loc)
self.gen.fact(fact)
```

And as I stated above, if including the parent name is not sufficient for
uniqueness we will need to go back and generate unique ids and add `has_child`
relationships.


## Other interfaces to consider?

Once the above is clear, I think I want to also call the following things interfaces:

 - DW_TAG_union_type
 - DW_TAG_class_type
 - DW_TAG_enumerator
 - DW_TAG_array_type

And each will probably need more special parsing. I'm not sure if I need to parse:

 - DW_TAG_member
 - DW_TAG_inheritance
 - DW_TAG_template_type_param
 - DW_TAG_template_value_param
 - DW_TAG_imported_module
 - DW_TAG_imported_declaration
 - DW_TAG_subrange_type
 - DW_TAG_subroutine_type (I'm currently skipping)
 - DW_TAG_inlined_subroutine (have not encountered yet, not parsing)
 - DW_TAG_enumeration_type (I suspect we will go through this when we parse enumerator interfaces)
 - DW_TAG_unspecified_type (possibly other types we will hit?)
 - DW_TAG_reference_type
 - DW_TAG_rvalue_reference_type
 - DW_TAG_GNU_call_site (no idea)
 - DW_TAG_GNU_call_site_parameter
 - DW_TAG_unspecified_parameters
 - DW_TAG_GNU_template_parameter_pack
 - DW_TAG_volatile_type (sounds dangerous!)
 - DW_TAG_lexical_block

I am not (directly) parsing:

 - DW_TAG_compile_unit
 - DW_TAG_namespace
 - DW_TAG_typedef
 - DW_TAG_base_type

Meaning I don't skip them entirely, but I haven't encountered them yet (unless it's
one of the DIEs that is passed through with a `DW_AT_type` that we return in the previous
step.) I suspect the typedef and base_type fall into this category.

Special cases - I only seem to hit these when I'm looking for a type. Others
from the last of "I'm not sure I need to parse" might appear here.

 - DW_AT_pointer_type
 - DW_AT_const_type
 - DW_AT_structure_type
