# Python DIR Zipper

---

## Details
### Version: 1.0
### Author: LASJ(pusaphil)
### Language: Python 3

---

## Description
<p>
For zipping (.zip) a directory with TXT and/or CSV files, and resizing/"parting" TXT and/or CSV files in given directory.
</p>

### Use case:
- Sending huge CSV report files over limited file attachement size email provider.

---

## Usage
### Syntax
```python
class DirZipper(this_dir, file_limit, zip_limit, get_header=True, delete_original=True, delete_part_files=True)
```
<p>
Where:
<pre>this_dir</pre>An existing string path.
<pre>file_limit</pre>Either integer or float value greater than 2000 bytes.
<pre>zip_limit</pre>Either integer or float value greater than 2000 bytes.
<pre>get_header</pre>Boolean. Indicator to get header of every TXT or/and CSV file. Default is True.
<pre>delete_original</pre>Boolean. Indicator to delete original TXT or/and CSV files. Default is True.
<pre>delete_part_files</pre>Boolean. Indicator to delete parted TXT or/and CSV files. Default is True.
</p>

### Sample Script (named test.py)
```python
    from dir_zipper import DirZipper

    # File resize value of 20000 bytes
    # Zip resize value of 50000 bytes
    sample = DirZipper('/foo/bar/output/20180209_200258', 20000, 50000)
    print(sample.start())
```

### Sample test dir
<p>In the scenario below, there is a directory named '20180209_200258' with two valid CSV files for zip and parting.</p>
```bash
pusa@some_cp:~/foo/bar/output/20180209_200258$ ll
total 212
drwxrwxr-x 3 pusa pusa   4096 Feb 13 08:54 ./
drwxrwxr-x 4 pusa pusa   4096 Feb 13 08:54 ../
-rw-rw-r-- 1 pusa pusa 100118 Feb 12 18:52 0BRBWK5ZQLTCPM0ANF2XIGEHVCQR514VU152LK0V9MVTJF32J406XL3CJZWITBSJ4KVQ03KWER3YQRTOBV02V0.csv
-rw-rw-r-- 1 pusa pusa      0 Feb 12 18:52 1.png
-rw-rw-r-- 1 pusa pusa 100086 Feb 12 18:52 G01R8IOCYDETNLA9OZC68BTF5HWXWBQLUJPKJHCLNNP.csv
drwxrwxr-x 2 pusa pusa   4096 Feb 12 18:52 Untitled Folder/
```

### Sample output of script
<p>(Sorry for the unwanted prints.)</p>

```bash
    Dir exists.
    /foo/bar/output/20180209_200258/0BRBWK5ZQLTCPM0ANF2XIGEHVCQR514VU152LK0V9MVTJF32J406XL3CJZWITBSJ4KVQ03KWER3YQRTOBV02V0.csv is supported.
    /foo/bar/output/20180209_200258/G01R8IOCYDETNLA9OZC68BTF5HWXWBQLUJPKJHCLNNP.csv is supported.
    ('{} is not supported. ', '/foo/bar/output/20180209_200258/Untitled Folder')
    ('{} is not supported. ', '/foo/bar/output/20180209_200258/1.png')
    File list is not empty.
    ('Deleting original file... %s', True)
    ('current_content: %s | %s', '/foo/bar/output/20180209_200258/0BRBWK5ZQLTCPM0ANF2XIGEHVCQR514VU152LK0V9MVTJF32J406XL3CJZWITBSJ4KVQ03KWER3YQRTOBV02V0.csv', True)
    ('Deleting original file... %s', True)
    ('current_content: %s | %s', '/foo/bar/output/20180209_200258/G01R8IOCYDETNLA9OZC68BTF5HWXWBQLUJPKJHCLNNP.csv', True)
    ('{} is not supported. ', '/foo/bar/output/20180209_200258/Untitled Folder')
    ('{} is not supported. ', '/foo/bar/output/20180209_200258/1.png')
    ('zip generated: %s', ['/foo/bar/output/20180209_200258_1.zip', '/foo/bar/output/20180209_200258_2.zip', '/foo/bar/output/20180209_200258_3.zip', '/foo/bar/output/20180209_200258_4.zip', '/foo/bar/output/20180209_200258_5.zip', '/foo/bar/output/20180209_200258_6.zip'])
    ('Delete part?: %s', True)
    Deleting part files...
    {'status': True, 'message': 'Dir exists. ', 'list_of_zip': ['/foo/bar/output/20180209_200258_1.zip', '/foo/bar/output/20180209_200258_2.zip', '/foo/bar/output/20180209_200258_3.zip', '/foo/bar/output/20180209_200258_4.zip', '/foo/bar/output/20180209_200258_5.zip', '/foo/bar/output/20180209_200258_6.zip']}
```

### Actual output
<p>One level up the directory used for testing, we can see the generated ZIP files</p>
```bash
    pusa@some_cp:~/foo/bar/output$ ll
    total 232
    drwxrwxr-x 4 pusa pusa  4096 Feb 13 08:56 ./
    drwxrwxr-x 5 pusa pusa  4096 Feb 13 08:42 ../
    drwxrwxr-x 3 pusa pusa  4096 Feb 13 08:56 20180209_200258/
    -rw-rw-r-- 1 pusa pusa 33966 Feb 13 08:56 20180209_200258_1.zip
    -rw-rw-r-- 1 pusa pusa 34111 Feb 13 08:56 20180209_200258_2.zip
    -rw-rw-r-- 1 pusa pusa 35212 Feb 13 08:56 20180209_200258_3.zip
    -rw-rw-r-- 1 pusa pusa 35474 Feb 13 08:56 20180209_200258_4.zip
    -rw-rw-r-- 1 pusa pusa 33836 Feb 13 08:56 20180209_200258_5.zip
    -rw-rw-r-- 1 pusa pusa 33901 Feb 13 08:56 20180209_200258_6.zip
```
<p>The directory used for testing will look like this. Noticed that the original files are deleted.</p>
```bash
    pusa@some_cp:~/foo/bar/output/20180209_200258$ ll
    total 12
    drwxrwxr-x 3 pusa pusa 4096 Feb 13 08:56 ./
    drwxrwxr-x 4 pusa pusa 4096 Feb 13 08:56 ../
    -rw-rw-r-- 1 pusa pusa    0 Feb 12 18:52 1.png
    drwxrwxr-x 2 pusa pusa 4096 Feb 12 18:52 Untitled Folder/

```