# Fix indentation in the Three Commas API client

import re

def fix_indentation(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Fix specific issues with indentation
    fixed_content = re.sub(r'(\n\s+)(?=def get_currency_rate)', '\n    ', content)
    
    with open(output_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"Fixed indentation and saved to {output_file}")

if __name__ == "__main__":
    fix_indentation('three_commas_client.py.bak', 'three_commas_client.py')
