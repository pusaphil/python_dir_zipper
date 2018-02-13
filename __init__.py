import os
import sys
import math
import zipfile


class DirZipper(object):
    def __init__(self, this_dir, file_limit, zip_limit, get_header=True, delete_original=True, delete_part_files=True):
        try:

            if self.is_dir(this_dir) is False:
                raise ValueError("Invalid Dir. ")

            check = self.__check_int_param('file_limit', file_limit)
            if check != '':
                raise ValueError(check)

            check = self.__check_int_param('zip_limit', zip_limit)
            if check != '':
                raise ValueError(check)

            self.__dir = this_dir
            self.__file_limit = file_limit
            self.__zip_limit = zip_limit

            self.__get_header = get_header
            self.__delete_original = delete_original
            self.__delete_part_files = delete_part_files

            self.__file_ext_supported_list = ('.txt', '.csv')
            self.__ret_val = {
                "status": True,
                "message": ""
            }
        except Exception as e:
            raise e

    def __check_int_param(self, key, val):
        ret_val = ''

        if (isinstance(val, int)) is False and (isinstance(val, float)) is False:
            ret_val += key + ' is not integer nor float. '

        elif val < 1999:
            ret_val += key + ' less than 1999. '

        return ret_val

    def start(self):
        if self.is_dir():
            self.__ret_val["message"] = "Dir exists. "
            print("Dir exists.")

            file_list = self.get_file_in_dir()

            if len(file_list) > 0:
                print("File list is not empty.")

                # Run file resizing
                self.resize_files(file_list, get_header=self.__get_header, delete_original=self.__delete_original)

                # Group files for zipping
                stat, ll, list_of_files = self.group_list_for_zip()

                if stat is True:
                    # Create zip files
                    stat, list_of_zip = self.create_zip(self.__dir, ll)

                    if stat is True:
                        print("zip generated: %s", list_of_zip)
                        self.__ret_val["list_of_zip"] = list_of_zip
                        print("Delete part?: %s", self.__delete_part_files)

                        if self.__delete_part_files:
                            print("Deleting part files...")
                            # Deleting part files
                            for item in list_of_files:
                                self.delete_file(item)
                    else:
                        print("No zip created. ")
                else:
                    self.__ret_val["status"] = False
                    self.__ret_val["message"] = "File list is empty. "

            else:
                self.__ret_val["status"] = False
                self.__ret_val["message"] = "File list is empty. "
        else:
            self.__ret_val["status"] = False
            self.__ret_val["message"] = "Dir does not exists. "

        return self.__ret_val

    def is_dir(self, this_dir=None):
        """Check dir if exists."""

        check_path = this_dir if this_dir is not None else self.__dir

        return os.path.exists(check_path)

    def get_file_in_dir(self, this_dir=None):
        """Get files that are supported in the given dir."""
        refined_file_list = list()

        this_dir = this_dir if this_dir is not None else self.__dir
        check_path = self.is_dir(this_dir)

        if check_path:
            list_dir = os.listdir(this_dir)
            for item in list_dir:
                item_path = this_dir + "/" + item
                if os.path.isfile(item_path) and item_path.lower().endswith(self.__file_ext_supported_list):
                    print("{} is supported.".format(item_path))
                    refined_file_list.append(item_path)
                else:
                    print("{} is not supported. ", item_path)
        else:
            print("Dir does not exists.")

        return refined_file_list

    def file_resize(self, this_filename, file_limit, get_header=True, delete_original=True):
        """Resize given file based on given limit. Resized file will have multiple parts. Original file will be deleted. """
        ret_val = True

        # this_file should exists and its file ext is supported, and is a file
        if os.path.exists(this_filename) is True and os.path.isfile(this_filename) and this_filename.lower().endswith(self.__file_ext_supported_list):
            original_file_size = os.stat(this_filename).st_size
            max_chunk = math.ceil(original_file_size / file_limit) + 1
            file_limit = math.ceil(original_file_size / max_chunk)
            filename, file_ext = os.path.splitext(this_filename)

            content = list()
            current_content = ''
            header_content = ''
            chunk_counter = 1

            with open(this_filename, 'r') as fh:
                content = fh.readlines()

            for row in content:

                if get_header:
                    header_content = row
                    get_header = False
                    file_limit -= sys.getsizeof(header_content)

                else:
                    current_content += row

                    if sys.getsizeof(current_content) > file_limit:
                        current_content = header_content + current_content
                        with open(filename + "_" + str(chunk_counter) + file_ext, "w") as file_chunk:
                            file_chunk.write(current_content)

                        current_content = ''
                        chunk_counter += 1

            if len(current_content) > 0:
                # Save to file the last data of current_content
                current_content = header_content + current_content
                with open(filename + "_" + str(chunk_counter) + file_ext, "w") as file_chunk:
                    file_chunk.write(current_content)

            # Delete original file
            if delete_original:
                print("Deleting original file... %s", self.delete_file(this_filename))

        else:
            ret_val = False

        return ret_val

    def resize_files(self, file_list=[], file_limit=None, get_header=True, delete_original=True):
        ret_val = True

        f_limit = file_limit if file_limit is not None else self.__file_limit

        if len(file_list) > 0:
            for file in file_list:
                print("current_content: %s | %s", file, self.file_resize(file, f_limit, get_header, delete_original))

        else:
            print("No list of files to resize.")
            ret_val = False

        return ret_val

    def delete_file(self, this_file):
        ret_val = True

        try:
            os.remove(this_file)
        except OSError as e:
            print(e)
            ret_val = False

        return ret_val

    def group_list_for_zip(self, this_dir=None, file_limit=None, zip_limit=None):
        """Group items in given dir by zip_limit. output is list of files for zipping."""
        ret_val = True
        list_of_list = []
        list_of_valid_files = []

        this_dir = this_dir if this_dir is not None else self.__dir
        file_limit = file_limit if file_limit is not None else self.__file_limit
        zip_limit = zip_limit if zip_limit is not None else self.__zip_limit

        if os.path.exists(this_dir):
            list_dir = os.listdir(this_dir)

            current_group = []
            current_group_size = 0

            if len(list_dir) > 0:
                for item in list_dir:
                    item_path = this_dir + "/" + item
                    item_size = os.stat(item_path).st_size

                    if os.path.isfile(item_path) and item_path.lower().endswith(self.__file_ext_supported_list) and item_size < file_limit:
                        list_of_valid_files.append(item_path)

                        if item_size + current_group_size < zip_limit:
                            current_group.append(item_path)
                            current_group_size += item_size
                        else:
                            list_of_list.append(current_group)
                            current_group = [item_path]
                            current_group_size = item_size
                    else:
                        print("{} is not supported. ", item_path)

                if len(current_group) > 0:
                    list_of_list.append(current_group)
        else:
            print("Dir does not exists.")
            ret_val = False

        return ret_val, list_of_list, list_of_valid_files

    def create_zip(self, zip_name, ll_files):
        """Create zip file from list of list of files."""
        ret_val = True
        list_of_zip = list()

        counter = 1
        for file_set in ll_files:

            if len(file_set) > 0:
                zip_file = zip_name + "_" + str(counter) + ".zip"
                zf = zipfile.ZipFile(zip_file, "w")

                for item in file_set:
                    zf.write(item, os.path.basename(item))

                list_of_zip.append(zip_file)
                counter += 1
            else:
                print("file_set is empty.")

        return ret_val, list_of_zip
