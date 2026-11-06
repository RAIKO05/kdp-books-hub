"""
build_kdp_release_packages.py
Generates official production distribution packages (.zip) for all 7 series.
Each zip package contains:
- Print-Ready Interior PDFs (176 Pages)
- Print-Ready Full-Wrap Cover PDFs (12.646" x 9.250")
- High-Res Front Cover Previews
- KDP_Listing_Metadata.txt for every volume
- Complete series manifest JSON
"""

import os
import zipfile
import json
import time

DIST_DIR = "KDP_Production_Packages"
os.makedirs(DIST_DIR, exist_ok=True)

SERIES_FOLDERS = [
    ("The_Detectives_Case_Files_Series", "The_Detectives_Case_Files_15_Volumes_KDP_Pack.zip"),
    ("Project_X", "Project_X_15_Volumes_KDP_Pack.zip"),
    ("The_Ravencrest_Chronicles", "The_Ravencrest_Chronicles_15_Volumes_KDP_Pack.zip"),
    ("The_Bletchley_Protocols", "The_Bletchley_Protocols_15_Volumes_KDP_Pack.zip"),
    ("Crypt_of_the_Pharaohs", "Crypt_of_the_Pharaohs_15_Volumes_KDP_Pack.zip"),
    ("The_Blackwood_Asylum_Files", "The_Blackwood_Asylum_Files_15_Volumes_KDP_Pack.zip"),
    ("The_Grand_Orient_Express", "The_Grand_Orient_Express_10_Volumes_KDP_Pack.zip"),
    ("The_Lupin_Heists", "The_Lupin_Heists_15_Volumes_KDP_Pack.zip"),
    ("The_Machine_Protocols", "The_Machine_Protocols_15_Volumes_KDP_Pack.zip")
]

def build_packages():
    print("=" * 80)
    print("   BUILDING PRODUCTION KDP DISTRIBUTION ZIP PACKAGES")
    print("=" * 80)
    t0 = time.time()

    packages_built = []

    for s_folder, zip_name in SERIES_FOLDERS:
        zip_path = os.path.join(DIST_DIR, zip_name)
        print(f"\n[*] Packaging {s_folder} -> {zip_name}...")
        
        file_count = 0
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(s_folder):
                for f in files:
                    # Include production PDFs, metadata, and preview images
                    if f.endswith(".pdf") or f.endswith(".txt") or f.endswith(".png") or f.endswith(".json"):
                        # Skip large intermediate caches or temp files
                        if "temp" in f or "__pycache__" in root: continue
                        abs_f = os.path.join(root, f)
                        rel_f = os.path.relpath(abs_f, s_folder)
                        zf.write(abs_f, rel_f)
                        file_count += 1
        
        size_mb = round(os.path.getsize(zip_path) / (1024 * 1024), 2)
        print(f"  [✓] Created {zip_name}: {file_count} files ({size_mb} MB)")
        packages_built.append((zip_name, size_mb, file_count))

    # Also build Master 130-Book Catalog Zip
    master_zip_path = os.path.join(DIST_DIR, "Master_130_Book_Catalog_Full_Production_Suite.zip")
    print(f"\n[*] Packaging Master 130-Book Catalog Suite...")
    m_count = 0
    with zipfile.ZipFile(master_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write("catalog.json", "catalog.json")
        for s_folder, _ in SERIES_FOLDERS:
            for root, dirs, files in os.walk(s_folder):
                for f in files:
                    if f.endswith(".pdf") or f.endswith(".txt") or f.endswith(".png") or f == "multigame_cases.json":
                        abs_f = os.path.join(root, f)
                        rel_f = os.path.relpath(abs_f, ".")
                        zf.write(abs_f, rel_f)
                        m_count += 1
    m_size_mb = round(os.path.getsize(master_zip_path) / (1024 * 1024), 2)
    print(f"  [✓] Created Master 130-Book Catalog Suite: {m_count} files ({m_size_mb} MB)")
    packages_built.append(("Master_130_Book_Catalog_Full_Production_Suite.zip", m_size_mb, m_count))

    # Also maintain legacy filename for existing link compatibility
    import shutil
    shutil.copyfile(master_zip_path, os.path.join(DIST_DIR, "Master_100_Book_Catalog_Full_Production_Suite.zip"))

    elapsed = round(time.time() - t0, 2)
    print("=" * 80)
    print("PACKAGING SUMMARY:")
    for pname, psize, pfiles in packages_built:
        print(f"  • {pname:<50} | {psize:>5.2f} MB | {pfiles:>4d} files")
    print(f"\nTotal elapsed time: {elapsed} seconds")
    print(f"Output directory: {os.path.abspath(DIST_DIR)}")
    print("=" * 80)

if __name__ == "__main__":
    build_packages()
