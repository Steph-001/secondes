#!/usr/bin/env python3
import os
import re
import sys

def get_frontmatter_and_content(file_path):
    """Extract frontmatter and remaining content from the file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return None, content
    
    frontmatter_text = match.group(1)
    remaining_content = match.group(2)
    
    return frontmatter_text, remaining_content

def add_lexicon_entries(file_path):
    """Add new lexicon entries to the file."""
    frontmatter_text, remaining_content = get_frontmatter_and_content(file_path)
    if frontmatter_text is None:
        print(f"Error: Could not find frontmatter in {file_path}")
        return
    
    # Check if lexicon section exists
    lexicon_exists = re.search(r'lexicon:', frontmatter_text) is not None
    
    # Prepare new entries
    new_entries = []
    print("\nAdding new lexicon entries. Type 'done' for the term to finish.")
    while True:
        term = input("\nEnter term (or 'done' to finish): ").strip()
        if term.lower() == 'done':
            break
        
        definition = input("Enter definition: ").strip()
        
        # Format new entry
        entry = f'    - term: "{term}"\n      definition: "{definition}"'
        new_entries.append(entry)
        
        print(f"Added: {term} - {definition}")
    
    if not new_entries:
        print("No entries added.")
        return
    
    # Update frontmatter
    if lexicon_exists:
        # Find the last entry in the lexicon section
        last_entry = re.search(r'(lexicon:.*?)(\n[a-zA-Z]|$)', frontmatter_text, re.DOTALL)
        if last_entry:
            insert_point = last_entry.start(2)
            updated_frontmatter = (
                frontmatter_text[:insert_point] + 
                "\n" + "\n".join(new_entries) + 
                frontmatter_text[insert_point:]
            )
        else:
            # If we can't find the end, just append to the lexicon line
            updated_frontmatter = re.sub(
                r'lexicon:', 
                'lexicon:\n' + "\n".join(new_entries), 
                frontmatter_text, 
                1
            )
    else:
        # Add lexicon section at the end of frontmatter
        updated_frontmatter = frontmatter_text.strip() + "\nlexicon:\n" + "\n".join(new_entries)
    
    # Create backup
    backup_path = file_path + ".bak"
    with open(backup_path, 'w', encoding='utf-8') as backup_file:
        with open(file_path, 'r', encoding='utf-8') as original_file:
            backup_file.write(original_file.read())
    
    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"---\n{updated_frontmatter}\n---\n{remaining_content}")
    
    print(f"\nFile updated successfully. Backup saved as {backup_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 lexicon.py <path_to_markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    add_lexicon_entries(file_path)

if __name__ == "__main__":
    main()
