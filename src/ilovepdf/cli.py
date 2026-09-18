import argparse
import sys
from ilovepdf.progress_bar import merge_with_progress, split_with_progress, compress_with_progress

def main():
    parser = argparse.ArgumentParser(description="CLI tool for PDF manipulation")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDF files")
    merge_parser.add_argument("input_files", nargs="+", help="Input PDF files")
    merge_parser.add_argument("-o", "--out", dest="output_path", required=True, help="Output PDF file")

    # split command
    split_parser = subparsers.add_parser("split", help="Split a PDF into pages")
    split_parser.add_argument("input_file", help="Input PDF file")
    split_parser.add_argument("-o", "--out", dest="output_dir", required=True, help="Output directory")

    # compress command
    compress_parser = subparsers.add_parser("compress", help="Compress a PDF")
    compress_parser.add_argument("input_file", help="Input PDF file")
    compress_parser.add_argument("-o", "--out", dest="output_path", required=True, help="Output PDF file")
    compress_parser.add_argument("--quality", choices=["low", "medium", "high"], default="medium", help="Compression quality")

    # list command
    list_parser = subparsers.add_parser("list", help="List available tools")

    args = parser.parse_args()

    if args.command == "list" or not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "merge":
            success = merge_with_progress(args.input_files, args.output_path)
            if not success:
                print("Error: Merge operation failed.", file=sys.stderr)
                sys.exit(1)
        elif args.command == "split":
            res = split_with_progress(args.input_file, args.output_dir)
            if not res:
                print("Error: Split operation failed.", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Successfully split into {len(res)} pages in {args.output_dir}")
        elif args.command == "compress":
            success = compress_with_progress(args.input_file, args.output_path, quality=args.quality)
            if not success:
                print("Error: Compress operation failed.", file=sys.stderr)
                sys.exit(1)
    except Exception as e:
        print(f"Command failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
