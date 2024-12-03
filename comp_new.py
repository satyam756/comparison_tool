import os
import filecmp
import difflib

# Author: Satyam Tripathi
# Date: 2024-12-03
# Description: This class compares two folders and generates a text file for each file that differs between the folders.

class FolderComparator:
    def __init__(self, folder1, folder2, output_folder):
        self.folder1 = folder1
        self.folder2 = folder2
        self.output_folder = output_folder
        self.folder1_files = set(os.listdir(folder1))
        self.folder2_files = set(os.listdir(folder2))
        self.common_files = self.folder1_files.intersection(self.folder2_files)
        self.only_in_folder1 = self.folder1_files - self.folder2_files
        self.only_in_folder2 = self.folder2_files - self.folder1_files

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def compare_files(self):
        for file in self.common_files:
            file1 = os.path.join(self.folder1, file)
            file2 = os.path.join(self.folder2, file)
            if os.path.isfile(file1) and os.path.isfile(file2):
                if filecmp.cmp(file1, file2, shallow=False):
                    print(f"{file} is identical in both folders")
                else:
                    print(f"{file} differs between folders")
                    self.write_differences(file1, file2, file)

    def write_differences(self, file1, file2, filename):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            diff = difflib.HtmlDiff().make_file(
                f1.readlines(),
                f2.readlines(),
                fromdesc=file1,
                todesc=file2
            )
            output_file = os.path.join(self.output_folder, f"{filename}.html")
            with open(output_file, 'w') as output:
                output.write(diff)

    def print_unique_files(self):
        for file in self.only_in_folder1:
            print(f"{file} is only in {self.folder1}")
        for file in self.only_in_folder2:
            print(f"{file} is only in {self.folder2}")

    def run_comparison(self):
        self.compare_files()
        self.print_unique_files()

if __name__ == "__main__":
    folder1 = input("Enter the path of the first folder: ")
    folder2 = input("Enter the path of the second folder: ")
    output_folder = "new_output"
    comparator = FolderComparator(folder1, folder2, output_folder)
    comparator.run_comparison()
