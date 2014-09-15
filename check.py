import sys
import os
import pprint

def index_directory(path):
    files = {}

    for root, subdirs, file_names in os.walk(path):
        for subdir in subdirs:
            for key, paths in index_directory(os.path.join(root, subdir)).items():
                if files.get(key) is None:
                    files[key] = set(paths)
                else:
                    files[key] |= set(paths)
        for file_name in file_names:
            full_path = os.path.join(root, file_name)
            size = os.stat(full_path).st_size
            key = '{},{}'.format(size, file_name)
            if files.get(key) is None:
                files[key] = set([])
            files[key] |= set([full_path])
    return files

def compare_indexes(old_files, new_files):
    old_keys = set(old_files.keys())
    new_keys = set(new_files.keys())

    missing_in_new = old_keys - new_keys
    both = old_keys & new_keys
    missing_in_old = new_keys - old_keys

    print('Missing in old:')
    for key in missing_in_old:
        pprint.pprint(new_files[key])
        print()

    print('Missing in new:')
    for key in missing_in_new:
        pprint.pprint(old_files[key])
        print()

    print('Present in both:')
    for key in both:
        pprint.pprint(old_files[key])
        pprint.pprint(new_files[key])
        print()

def run_check(old, new):
    print('Indexing new directory...')
    new_files = index_directory(new)
    #pprint.pprint(new_files)

    print('Indexing old directory...')
    old_files = index_directory(old)
    #pprint.pprint(old_files)
    
    compare_indexes(old_files, new_files)

if __name__ == '__main__':
    old = sys.argv[1]
    new = sys.argv[2]
    print('Comparing old location {} to new location {}'.format(old, new))
    run_check(old, new)
