import os
import re

def find_actual_merge_conflicts(directory='.'):
    """Find files with actual merge conflict markers."""
    # Pattern to match actual merge conflict blocks
    conflict_pattern = re.compile(
        r'^<<<<<<< .*$(.*?)^=======$(.*?)^>>>>>>> .*$', 
        re.MULTILINE | re.DOTALL
    )
    
    files_with_conflicts = []
    
    # Walk through all files in the directory
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
        
        for file in files:
            # Skip binary files and common build artifacts
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.exe', '.dll', '.so', '.dylib', '.bat', '.ps1')):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Look for actual conflict blocks
                    matches = conflict_pattern.findall(content)
                    if matches:
                        files_with_conflicts.append((file_path, len(matches)))
            except Exception as e:
                # Skip files that can't be read as text
                continue
    
    return files_with_conflicts

def show_conflict_details(directory='.'):
    """Show detailed information about conflicts."""
    # Pattern to match actual merge conflict blocks
    conflict_pattern = re.compile(
        r'^(<<<<<<< .*?)$(.*?)^(=======)$()(.*?)^(>>>>>>> .*?)$', 
        re.MULTILINE | re.DOTALL
    )
    
    files_with_conflicts = []
    
    # Walk through all files in the directory
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
        
        for file in files:
            # Skip binary files and common build artifacts
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.exe', '.dll', '.so', '.dylib', '.bat', '.ps1')):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Look for actual conflict blocks
                    for match in conflict_pattern.finditer(content):
                        files_with_conflicts.append((file_path, match.group(0)[:100]))  # First 100 chars
            except Exception as e:
                # Skip files that can't be read as text
                continue
    
    return files_with_conflicts

if __name__ == '__main__':
    print("=== CHECKING FOR ACTUAL MERGE CONFLICTS ===")
    conflicts = find_actual_merge_conflicts('.')
    
    if conflicts:
        print(f"\nFound {len(conflicts)} files with merge conflicts:")
        for file_path, count in conflicts:
            print(f"  {file_path} ({count} conflict{'s' if count > 1 else ''})")
        
        print("\n=== DETAILED CONFLICT PREVIEWS ===")
        detailed_conflicts = show_conflict_details('.')
        for file_path, conflict_preview in detailed_conflicts[:5]:  # Show first 5
            print(f"\n{file_path}:")
            print(f"  {conflict_preview}...")
    else:
        print("No actual merge conflicts found in the repository.")