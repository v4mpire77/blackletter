import os
import glob

def check_for_merge_conflicts(directory='.'):
    """Check for merge conflict markers in all files in the directory."""
    conflict_markers = ['<<<<<<<', '=======', '>>>>>>>']
    files_with_conflicts = []
    
    # Walk through all files in the directory
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
        
        for file in files:
            # Skip binary files and common build artifacts
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.exe', '.dll', '.so', '.dylib')):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        for marker in conflict_markers:
                            if marker in line:
                                files_with_conflicts.append((file_path, line_num, line.strip()))
                                break
            except Exception as e:
                # Skip files that can't be read as text
                continue
    
    return files_with_conflicts

if __name__ == '__main__':
    conflicts = check_for_merge_conflicts('.')
    
    if conflicts:
        print("Files with merge conflicts found:")
        for file_path, line_num, content in conflicts:
            print(f"{file_path}:{line_num}: {content}")
    else:
        print("No merge conflicts found in the repository.")