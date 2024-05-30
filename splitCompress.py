"""
Attachment split compress
"""
import os
import zipfile

dir_to_zip = os.environ["FILE_SAVE_DIR"]

output_dir = os.environ["ARCHIVE_SPLIT_ZIP_DIR"]

# Size limit for zip files (in bytes)
size_limit = 200 * 1024 * 1024  # 200MB

zip_file_counter = 1
current_zip_size = 0

zip_file = zipfile.ZipFile(f"{output_dir}/archive_{zip_file_counter}.zip", 'w', zipfile.ZIP_DEFLATED)

for root, dirs, files in os.walk(dir_to_zip):
    for file in files:
        file_path = os.path.join(root, file)

        if current_zip_size + os.path.getsize(file_path) > size_limit:
            zip_file.close()

            zip_file_counter += 1

            zip_file = zipfile.ZipFile(f"{output_dir}/archive_{zip_file_counter}.zip", 'w', zipfile.ZIP_DEFLATED)

            current_zip_size = 0

        zip_file.write(file_path, arcname=os.path.relpath(file_path, dir_to_zip))

        current_zip_size += os.path.getsize(file_path)

zip_file.close()
