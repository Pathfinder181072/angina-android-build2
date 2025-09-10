# -*- coding: utf-8 -*-
"""
ANGINA™ File Splitter - Professional Edition
Your Magical Solution for File Splitting Needs
"""

import os
import math
import time
import glob
import sys
import subprocess
from pathlib import Path

# Check and install required packages
try:
    from tqdm import tqdm
    import colorama
    from colorama import Fore, Back, Style
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter
except ImportError:
    print("📦 Installing required packages...")
    packages = ['tqdm', 'colorama', 'pygments']
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            sys.exit(1)
    
    # Now import the packages
    from tqdm import tqdm
    import colorama
    from colorama import Fore, Back, Style
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter

# Initialize colorama
colorama.init(autoreset=True)

class FileSplitter:
    def __init__(self):
        self.input_folder = "Input"
        self.output_folder = "Output"
        self.create_folders()
        
    def create_folders(self):
        """Create Input and Output folders if they don't exist"""
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)
            print(Fore.YELLOW + f"📁 Created {self.input_folder} folder - Please add your files there!")
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def display_banner(self):
        """Display a stylish banner for the application"""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""
    {Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║{Fore.RED}                 █████╗ ███╗   ██╗ ██████╗ ██╗███╗   ██╗ █████╗{Fore.CYAN}║
    ║{Fore.RED}                ██╔══██╗████╗  ██║██╔════╝ ██║████╗  ██║██╔══██╗{Fore.CYAN}║
    ║{Fore.RED}                ███████║██╔██╗ ██║██║  ███╗██║██╔██╗ ██║███████║{Fore.CYAN}║
    ║{Fore.RED}                ██╔══██║██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══██║{Fore.CYAN}║
    ║{Fore.RED}                ██║  ██║██║ ╚████║╚██████╔╝██║██║ ╚████║██║  ██║{Fore.CYAN}║
    ║{Fore.RED}                ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝{Fore.CYAN}║
    ║                                                              ║
    ║{Fore.YELLOW}                 ✂️  F I L E   S P L I T T E R  ✂️            {Fore.CYAN}║
    ║                                                              ║
    ║{Fore.GREEN}                 Your Magical Solution                        {Fore.CYAN}║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    {Style.RESET_ALL}"""
        print(banner)
    
    def get_files_in_input(self, extensions=['.txt', '.csv', '.log', '.json', '.xml', '.py', '.html', '.js', '.css']):
        """Get list of files in the Input folder"""
        all_files = []
        for ext in extensions:
            all_files.extend(glob.glob(os.path.join(self.input_folder, f"*{ext}")))
        return sorted(all_files)
    
    def preview_file(self, file_path, lines=5):
        """Preview the first few lines of a file with syntax highlighting"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = ''.join([next(f) for _ in range(lines)])
            
            # Try to detect file type for syntax highlighting
            file_ext = os.path.splitext(file_path)[1].lower()
            lexer_name = "text"
            if file_ext == '.py': lexer_name = "python"
            elif file_ext == '.json': lexer_name = "json"
            elif file_ext == '.xml': lexer_name = "xml"
            elif file_ext == '.csv': lexer_name = "csv"
            elif file_ext == '.html': lexer_name = "html"
            elif file_ext == '.js': lexer_name = "javascript"
            elif file_ext == '.css': lexer_name = "css"
            
            lexer = get_lexer_by_name(lexer_name, stripall=True)
            formatter = TerminalFormatter()
            highlighted = highlight(content, lexer, formatter)
            
            print(f"\n{Fore.CYAN}📄 Preview of {os.path.basename(file_path)} (first {lines} lines):{Style.RESET_ALL}")
            print("-" * 60)
            print(highlighted)
            print("-" * 60)
            
        except Exception as e:
            print(f"{Fore.RED}❌ Could not preview file: {e}{Style.RESET_ALL}")
    
    def select_files(self, files):
        """Display files and let user select multiple files"""
        if not files:
            print(f"{Fore.YELLOW}❌ No supported files found in the {self.input_folder} folder.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Supported formats: .txt, .csv, .log, .json, .xml, .py, .html, .js, .css{Style.RESET_ALL}")
            return None
        
        print(f"\n{Fore.CYAN}📋 Files available in {self.input_folder} folder:{Style.RESET_ALL}")
        for i, file_path in enumerate(files, 1):
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            size_str = self.format_file_size(file_size)
            print(f"{Fore.WHITE}   {i}. {file_name} ({size_str}){Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}\n🎯 Selection options:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   - Enter single number (e.g., 1){Style.RESET_ALL}")
        print(f"{Fore.WHITE}   - Multiple numbers separated by commas (e.g., 1,3,5){Style.RESET_ALL}")
        print(f"{Fore.WHITE}   - Range with hyphen (e.g., 1-3){Style.RESET_ALL}")
        print(f"{Fore.WHITE}   - 'all' to process all files{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   - 'preview X' to preview file number X (e.g., 'preview 1'){Style.RESET_ALL}")
        
        try:
            choice = input(f"\n{Fore.GREEN}👉 Enter your selection: {Style.RESET_ALL}").strip().lower()
            
            if choice == 'all':
                return files
            
            elif choice.startswith('preview'):
                parts = choice.split()
                if len(parts) > 1 and parts[1].isdigit():
                    file_idx = int(parts[1]) - 1
                    if 0 <= file_idx < len(files):
                        self.preview_file(files[file_idx])
                        input(f"\n{Fore.YELLOW}⏳ Press Enter to continue...{Style.RESET_ALL}")
                        return self.select_files(files)
                return None
            
            elif '-' in choice:
                # Handle range selection (e.g., 1-3)
                start, end = map(int, choice.split('-'))
                selected_files = files[start-1:end]
                return selected_files
            
            elif ',' in choice:
                # Handle multiple selection (e.g., 1,3,5)
                indices = [int(x.strip()) for x in choice.split(',')]
                selected_files = [files[i-1] for i in indices if 1 <= i <= len(files)]
                return selected_files if selected_files else None
            
            else:
                # Handle single selection
                choice_num = int(choice)
                if 1 <= choice_num <= len(files):
                    return [files[choice_num-1]]
                else:
                    print(f"{Fore.RED}❌ Invalid selection.{Style.RESET_ALL}")
                    return None
                    
        except ValueError:
            print(f"{Fore.RED}❌ Please enter valid numbers.{Style.RESET_ALL}")
            return None
    
    def format_file_size(self, size_bytes):
        """Convert file size to human-readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def get_split_method(self):
        """Let user choose the split method"""
        print(f"\n{Fore.CYAN}📊 Choose split method:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   1. By number of pieces (default){Style.RESET_ALL}")
        print(f"{Fore.WHITE}   2. By number of lines per piece{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   3. By file size per piece (e.g., 5MB, 1GB){Style.RESET_ALL}")
        print(f"{Fore.WHITE}   4. By content pattern (split at specific text){Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}👉 Enter method number (1-4): {Style.RESET_ALL}").strip()
        
        if choice == '2':
            try:
                lines_per_piece = int(input(f"{Fore.GREEN}👉 Enter number of lines per piece: {Style.RESET_ALL}"))
                return {'method': 'lines', 'value': lines_per_piece}
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")
                return self.get_split_method()
        
        elif choice == '3':
            size_input = input(f"{Fore.GREEN}👉 Enter size (e.g., 5MB, 1GB, 500KB): {Style.RESET_ALL}").strip().upper()
            try:
                if size_input.endswith('KB'):
                    size = int(size_input[:-2]) * 1024
                elif size_input.endswith('MB'):
                    size = int(size_input[:-2]) * 1024 * 1024
                elif size_input.endswith('GB'):
                    size = int(size_input[:-2]) * 1024 * 1024 * 1024
                else:
                    size = int(size_input)  # Assume bytes if no unit
                return {'method': 'size', 'value': size}
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid size.{Style.RESET_ALL}")
                return self.get_split_method()
        
        elif choice == '4':
            pattern = input(f"{Fore.GREEN}👉 Enter pattern to split at: {Style.RESET_ALL}").strip()
            return {'method': 'pattern', 'value': pattern}
        
        else:
            try:
                num_pieces = int(input(f"{Fore.GREEN}👉 Enter number of pieces: {Style.RESET_ALL}"))
                return {'method': 'pieces', 'value': num_pieces}
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")
                return self.get_split_method()
    
    def get_naming_pattern(self, original_name):
        """Let user choose custom naming pattern"""
        print(f"\n{Fore.CYAN}📝 Choose naming pattern:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   1. Default (filename_partX.ext){Style.RESET_ALL}")
        print(f"{Fore.WHITE}   2. Sequential (filename_001.ext, filename_002.ext){Style.RESET_ALL}")
        print(f"{Fore.WHITE}   3. Custom pattern{Style.RESET_ALL}")
        
        choice = input(f"{Fore.GREEN}👉 Enter choice (1-3): {Style.RESET_ALL}").strip()
        
        if choice == '2':
            return "{name}_{num:03d}{ext}"
        elif choice == '3':
            pattern = input(f"{Fore.GREEN}👉 Enter pattern (use {{name}} for filename, {{num}} for part number, {{ext}} for extension): {Style.RESET_ALL}")
            return pattern
        else:
            return "{name}_part{num}{ext}"
    
    def split_animation(self):
        """Display a splitting animation"""
        frames = ["✂️  Splitting |", "✂️  Splitting /", "✂️  Splitting -", "✂️  Splitting \\"]
        for _ in range(3):
            for frame in frames:
                print(f"\r{Fore.YELLOW}{frame}", end="", flush=True)
                time.sleep(0.1)
        print("\r" + " " * 20 + "\r", end="", flush=True)
    
    def split_file(self, file_path, split_method, naming_pattern):
        """Split a file using the specified method"""
        file_name = os.path.basename(file_path)
        base_name, ext = os.path.splitext(file_name)
        file_size = os.path.getsize(file_path)
        
        # Replace placeholders in naming pattern
        output_pattern = naming_pattern.replace("{name}", base_name)
        output_pattern = output_pattern.replace("{ext}", ext)
        
        size_str = self.format_file_size(file_size)
        print(f"\n{Fore.BLUE}📊 Processing '{file_name}' ({size_str})...{Style.RESET_ALL}")
        
        if split_method['method'] == 'pieces':
            self.split_by_pieces_improved(file_path, split_method['value'], output_pattern)
        elif split_method['method'] == 'lines':
            self.split_by_lines(file_path, split_method['value'], output_pattern)
        elif split_method['method'] == 'size':
            self.split_by_size(file_path, split_method['value'], output_pattern)
        elif split_method['method'] == 'pattern':
            self.split_by_pattern(file_path, split_method['value'], output_pattern)
    
    def split_by_pieces_improved(self, file_path, num_pieces, output_pattern):
        """Improved splitting with better size management"""
        file_size = os.path.getsize(file_path)
        target_piece_size = file_size / num_pieces
        
        print(f"{Fore.CYAN}🎯 Target piece size: {self.format_file_size(target_piece_size)}{Style.RESET_ALL}")
        
        with open(file_path, 'rb') as f:
            content = f.read()
        
        with tqdm(total=num_pieces, desc=f"{Fore.CYAN}Splitting", unit="piece", bar_format='{l_bar}{bar:40}{r_bar}{bar:-40b}') as pbar:
            for i in range(num_pieces):
                start = int(i * target_piece_size)
                end = int((i + 1) * target_piece_size) if i < num_pieces - 1 else file_size
                
                # For text files, try to split at a line break
                if i < num_pieces - 1:
                    # Look for the nearest newline character
                    newline_pos = content.find(b'\n', end)
                    if newline_pos != -1 and newline_pos < file_size:
                        end = newline_pos + 1  # Include the newline
                
                piece_content = content[start:end]
                
                output_filename = os.path.join(
                    self.output_folder, 
                    output_pattern.replace("{num}", str(i+1))
                )
                
                with open(output_filename, 'wb') as output_file:
                    output_file.write(piece_content)
                
                piece_size = len(piece_content)
                size_str = self.format_file_size(piece_size)
                pbar.set_postfix_str(f"{size_str}")
                pbar.update(1)
        
        # Verify and display results
        self.verify_split_results(file_path, num_pieces, output_pattern)
    
    def split_by_lines(self, file_path, lines_per_piece, output_pattern):
        """Split file by number of lines per piece"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as original_file:
            lines = original_file.readlines()
            total_lines = len(lines)
            num_pieces = math.ceil(total_lines / lines_per_piece)
            
            with tqdm(total=num_pieces, desc=f"{Fore.CYAN}Splitting", unit="piece", bar_format='{l_bar}{bar:40}{r_bar}{bar:-40b}') as pbar:
                for i in range(num_pieces):
                    start_idx = i * lines_per_piece
                    end_idx = min((i + 1) * lines_per_piece, total_lines)
                    
                    output_filename = os.path.join(
                        self.output_folder, 
                        output_pattern.replace("{num}", str(i+1))
                    )
                    
                    with open(output_filename, 'w', encoding='utf-8') as output_file:
                        output_file.writelines(lines[start_idx:end_idx])
                    
                    pbar.update(1)
        
        print(f"{Fore.GREEN}✅ Split into {num_pieces} pieces with {lines_per_piece} lines each{Style.RESET_ALL}")
    
    def split_by_size(self, file_path, piece_size, output_pattern):
        """Split file by size per piece"""
        file_size = os.path.getsize(file_path)
        num_pieces = math.ceil(file_size / piece_size)
        
        print(f"{Fore.CYAN}🎯 Target piece size: {self.format_file_size(piece_size)}{Style.RESET_ALL}")
        
        with open(file_path, 'rb') as f:
            content = f.read()
        
        with tqdm(total=num_pieces, desc=f"{Fore.CYAN}Splitting", unit="piece", bar_format='{l_bar}{bar:40}{r_bar}{bar:-40b}') as pbar:
            for i in range(num_pieces):
                start = i * piece_size
                end = min((i + 1) * piece_size, file_size)
                
                # For text files, try to split at a line break
                if i < num_pieces - 1:
                    # Look for the nearest newline character
                    newline_pos = content.find(b'\n', end)
                    if newline_pos != -1 and newline_pos < file_size:
                        end = newline_pos + 1  # Include the newline
                
                piece_content = content[start:end]
                
                output_filename = os.path.join(
                    self.output_folder, 
                    output_pattern.replace("{num}", str(i+1))
                )
                
                with open(output_filename, 'wb') as output_file:
                    output_file.write(piece_content)
                
                actual_size = len(piece_content)
                size_str = self.format_file_size(actual_size)
                pbar.set_postfix_str(f"{size_str}")
                pbar.update(1)
        
        # Verify and display results
        self.verify_split_results(file_path, num_pieces, output_pattern)
    
    def split_by_pattern(self, file_path, pattern, output_pattern):
        """Split file at specific pattern occurrences"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as original_file:
            content = original_file.read()
        
        parts = content.split(pattern)
        num_pieces = len(parts)
        
        with tqdm(total=num_pieces, desc=f"{Fore.CYAN}Splitting", unit="piece", bar_format='{l_bar}{bar:40}{r_bar}{bar:-40b}') as pbar:
            for i, part in enumerate(parts):
                if not part.strip():
                    continue
                
                output_filename = os.path.join(
                    self.output_folder, 
                    output_pattern.replace("{num}", str(i+1))
                )
                
                with open(output_filename, 'w', encoding='utf-8') as output_file:
                    output_file.write(part)
                
                pbar.update(1)
        
        print(f"{Fore.GREEN}✅ Split into {num_pieces} pieces at '{pattern}' pattern{Style.RESET_ALL}")
    
    def verify_split_results(self, original_file, num_pieces, output_pattern):
        """Verify and display split results"""
        original_size = os.path.getsize(original_file)
        split_files = []
        total_split_size = 0
        
        for i in range(1, num_pieces + 1):
            split_file_path = os.path.join(
                self.output_folder, 
                output_pattern.replace("{num}", str(i))
            )
            if os.path.exists(split_file_path):
                file_size = os.path.getsize(split_file_path)
                split_files.append((split_file_path, file_size))
                total_split_size += file_size
        
        print(f"\n{Fore.CYAN}📊 Split Results:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   Original file: {self.format_file_size(original_size)}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   Total split size: {self.format_file_size(total_split_size)}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   Size difference: {self.format_file_size(total_split_size - original_size)}{Style.RESET_ALL}")
        
        if split_files:
            print(f"\n{Fore.CYAN}📁 Split files:{Style.RESET_ALL}")
            for file_path, size in split_files:
                size_str = self.format_file_size(size)
                file_name = os.path.basename(file_path)
                print(f"{Fore.WHITE}   • {file_name} ({size_str}){Style.RESET_ALL}")
    
    def main_menu(self):
        """Main menu for the application"""
        while True:
            self.display_banner()
            files = self.get_files_in_input()
            
            if not files:
                input(f"\n{Fore.YELLOW}⏳ Press Enter to check again for files...{Style.RESET_ALL}")
                continue
            
            selected_files = self.select_files(files)
            if not selected_files:
                input(f"\n{Fore.YELLOW}⏳ Press Enter to try again...{Style.RESET_ALL}")
                continue
            
            split_method = self.get_split_method()
            naming_pattern = self.get_naming_pattern(os.path.basename(selected_files[0]))
            
            # Process all selected files
            total_files = len(selected_files)
            for idx, file_path in enumerate(selected_files, 1):
                print(f"\n{Fore.CYAN}📂 Processing file {idx} of {total_files}{Style.RESET_ALL}")
                self.split_file(file_path, split_method, naming_pattern)
            
            # Ask if user wants to continue or exit
            print(f"\n{Fore.CYAN}" + "="*60 + f"{Style.RESET_ALL}")
            choice = input(f"\n{Fore.GREEN}🔄 Would you like to process more files?\n{Fore.WHITE}   1. Yes, process more files\n{Fore.WHITE}   2. No, exit the program\n\n{Fore.GREEN}👉 Enter your choice (1 or 2): {Style.RESET_ALL}")
            
            if choice != '1':
                print(f"\n{Fore.MAGENTA}✨ Thank you for using ANGINA™ File Splitter!")
                print(f"{Fore.MAGENTA}   Have a great day! 👋{Style.RESET_ALL}")
                break

def main():
    """Main function"""
    try:
        splitter = FileSplitter()
        splitter.main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}👋 Program interrupted. Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()