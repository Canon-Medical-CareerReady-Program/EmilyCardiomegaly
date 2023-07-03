#
# Download the 56 zip files in Images_png in batches
#
import os
import urllib.request
import shutil
from pathlib import Path
import pandas as pd

def print_message(msg: str):
    print("---"*5)
    print(msg)
    print("---"*5)


def print_download_status(block_num, block_size, total_size):
    downloaded = block_num * block_size
    percent = 100.0 * downloaded / total_size
    downloaded_mb = downloaded / 1024 / 1024
    total_size_mb = total_size / 1024 / 1024
    print(f"\r      Downloaded {downloaded_mb:.2f} of {total_size_mb:.2f} mega bytes ({percent:.2f}%)      ", end='', flush=True)

# URLs for the zip files
img_links = [
    "https://nihcc.box.com/shared/static/vfk49d74nhbxq3nqjg0900w5nvkorp5c.gz",
    "https://nihcc.box.com/shared/static/i28rlmbvmfjbl8p2n3ril0pptcmcu9d1.gz",
    "https://nihcc.box.com/shared/static/f1t00wrtdk94satdfb9olcolqx20z2jp.gz",
    "https://nihcc.box.com/shared/static/0aowwzs5lhjrceb3qp67ahp0rd1l1etg.gz",
    "https://nihcc.box.com/shared/static/v5e3goj22zr6h8tzualxfsqlqaygfbsn.gz",
    "https://nihcc.box.com/shared/static/asi7ikud9jwnkrnkj99jnpfkjdes7l6l.gz",
    "https://nihcc.box.com/shared/static/jn1b4mw4n6lnh74ovmcjb8y48h8xj07n.gz",
    "https://nihcc.box.com/shared/static/tvpxmn7qyrgl0w8wfh9kqfjskv6nmm1j.gz",
    "https://nihcc.box.com/shared/static/upyy3ml7qdumlgk2rfcvlb9k6gvqq2pj.gz",
    "https://nihcc.box.com/shared/static/l6nilvfa9cg3s28tqv1qc1olm3gnz54p.gz",
    "https://nihcc.box.com/shared/static/hhq8fkdgvcari67vfhs7ppg2w6ni4jze.gz",
    "https://nihcc.box.com/shared/static/ioqwiy20ihqwyr8pf4c24eazhh281pbu.gz"
]
# Get the path to project root / Data
# (get file path, remove filename with first "parent", remove Scripts folder with second "parent")
data_base_dir = Path(__file__).parent.parent / "Data"

data_cache_dir = Path(os.environ.get('CAREER_READY_CACHE', data_base_dir / "Cache"))
print(f"Data cache directory: {data_cache_dir}")

os.makedirs(data_base_dir, exist_ok=True)
os.makedirs(data_cache_dir, exist_ok=True)

# This file was taken from https://nihcc.app.box.com/v/ChestXray-NIHCC we would download it from their
# but there isn't a stable link to download.
spreadsheet_path = data_base_dir / "BBox_List_2017.csv"

# Go over each row in the spreadsheet if any single image is missing then we will want
# download and unpack the tar.gz files.
need_unpack = False
dataframe = pd.read_csv(spreadsheet_path)
for idx, row in dataframe.iterrows():
    full_file_path = data_cache_dir / "images" / row["Image Index"]
    if full_file_path.exists() is False:
        print(f"File {full_file_path} does not exist!")
        need_unpack = True
        break

if need_unpack:
    # First we will check to see if the tar.gz files are already downloaded
    # this is the slow bit, so we do it one at a time.
    print_message("Checking if data needs to be downloaded...")
    showed_download_warning = False
    for idx, link in enumerate(img_links):
        print(f"  Checking input data bundle {idx + 1} of {len(img_links)}...")
        filename = data_cache_dir / f'images_{idx + 1}.tar.gz'
        if filename.exists() is False:
            if showed_download_warning is False:
                print("  Downloading data.\nPlease note there's a lot of data to download (approx 40GB), it might take a while.")
                showed_download_warning = True
            print(f"     Downloading {filename}...")
            # Download
            try:
                urllib.request.urlretrieve(link, filename, print_download_status)
                print(); # Just to get a newline because the download status doesn't print one
            except Exception as e:
                print(f"\n  Download failed: {e}")
                if os.path.isfile(filename):
                    os.remove(filename)
                    exit(1)

    for idx, link in enumerate(img_links):
        filename = data_cache_dir / f'images_{idx + 1}.tar.gz'
        print(f"Unpacking {idx + 1} of {len(img_links)}: {filename}...")
        shutil.unpack_archive(filename=filename, extract_dir=data_cache_dir)
else:
    print_message("Your cache is up to date.")

print_message(f"Finished. Your data is in {data_cache_dir}")
