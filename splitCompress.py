"""
Attachment split compress with verification
"""
import os
import zipfile

dir_to_zip = os.environ["FILE_SAVE_DIR"]
output_dir = os.environ["ATTACHMENT_SPLIT_ZIP_DIR"]

# Size limit for zip files (in bytes)
size_limit = 150 * 1024 * 1024  # 150MB

zip_file_counter = 1
current_zip_size = 0

zip_file_path = f"{output_dir}/attachment_{zip_file_counter}.zip"
zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

all_files = []

for root, dirs, files in os.walk(dir_to_zip):
    for file in files:
        file_path = os.path.join(root, file)
        all_files.append(file_path)

all_files.sort()

for file_path in all_files:
    if current_zip_size + os.path.getsize(file_path) > size_limit:
        zip_file.close()

        zip_file_counter += 1

        zip_file_path = f"{output_dir}/attachment_{zip_file_counter}.zip"
        zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

        current_zip_size = 0

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    try:
        zip_file.write(file_path, arcname=os.path.relpath(file_path, dir_to_zip))
    except FileNotFoundError:
        print(f"File not found when trying to write to zip file: {file_path}")
        continue

    current_zip_size += os.path.getsize(file_path)

zip_file.close()

# Verify Zip Files

# for i in range(1, zip_file_counter + 1):
#     zip_file_path = f"{output_dir}/attachment_{i}.zip"
#     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#         bad_file = zip_ref.testzip()
#         if bad_file:
#             print(f"Bad file found in {zip_file_path}: {bad_file}")


def test_zip_files(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        bad_files = []
        for file in zip_ref.namelist():
            try:
                zip_ref.read(file)
            except zipfile.BadZipFile:
                bad_files.append(file)
        return bad_files

for i in range(1, zip_file_counter + 1):
    zip_file_path = f"{output_dir}/attachment_{i}.zip"
    bad_files = test_zip_files(zip_file_path)
    if bad_files:
        print(f"Bad files found in {zip_file_path}: {bad_files}")
