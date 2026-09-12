import os
import zipfile

def package_submission(output_zip="Tech_Zephyr_4_Problem9_AegisSOC_Submission.zip"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.idea', '.vscode'}
    exclude_files = {'*.pyc', '*.db-journal'}

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(base_dir):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for f in files:
                if f.endswith(('.pyc', '.zip')):
                    continue
                file_path = os.path.join(root, f)
                arcname = os.path.relpath(file_path, base_dir)
                zf.write(file_path, arcname)

    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"Submission ZIP successfully generated: {output_zip} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package_submission()
