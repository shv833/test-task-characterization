## Requirements for prod mode
- Docker
- Make

## Requirements for dev mode
- Docker
- Make
- Python

## Getting started with Windows 10/11

```
winget install ezwinports.make
```

```
git clone https://github.com/shv833/test-task-characterization.git
```

```
cd ./test-task-characterization
```

## How to run app
```
make run
```
or for clean run(rebuild images and reinstall packages)
```
make crun
```

## Binary File Structure
The binary file structure consists of a sequence of records. Each record starts with a 4-byte header indicating the record type, followed by specific fields that vary depending on the header. Below is the structure of each record type:

MIR (Measurement Information Record)

Header (4 bytes): "MIR" (ASCII, null-padded if shorter).
Temperature (4 bytes): Floating-point value (IEEE 754).
Operator (20 bytes): ASCII string, null-padded.
PRR (Part Record)

Header (4 bytes): "PRR" (ASCII, null-padded if shorter).
Part Number (4 bytes): Unsigned integer.
Status (1 byte): Unsigned byte.
PTR (Parameter Test Record)

Header (4 bytes): "PTR" (ASCII, null-padded if shorter).
Test Name (20 bytes): ASCII string, null-padded.
Test Value (4 bytes): Floating-point value (IEEE 754).
Low Limit (4 bytes): Floating-point value (IEEE 754).
High Limit (4 bytes): Floating-point value (IEEE 754).
Status (1 byte): Unsigned byte.

## How to use app
0. Run app:)
1. Open link `http://localhost:8000/`
2. Press `Choose file`
3. Pick binary file from folder `app/test_data_bin`
4. Press `Upload file`
5. See the decoded file in a table view and next 4 buttons
`Show JSON View | Save Changes | Compare Files' Hashes | Clear session`
6. Button `Show JSON View` shows decoded information in json format
7. Button `Save Changes` saves info from table to new binary file 
8. Button `Clear session` clears current session, thus clearing the table
9. Button `Compare Files' Hashes` is extra page for checking whether two files are identical. Practical usage:
* Decode file in `http://localhost:8000/` page
* Do not change the data in the table and save decoded info to new binary file
* In the `http://localhost:8000/compare_hashes` page pick original file and new binary file in two file inputs
* Press `Compare hashes` button
* These two files must be identical, because nothing has changed before saving, and their hashes must be the same. If they are, decoding and encoding will work well and we won't lose the original data


P.S.
As an addition for this project, it would ne nice to implement next
TODO: 
1. multiple file upload?
2. limit values for each data type
3. proper handling float numbers
