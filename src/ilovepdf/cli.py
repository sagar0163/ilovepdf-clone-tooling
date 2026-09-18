import argparse
import sys
from ilovepdf.progress_bar import merge_with_progress, split_with_progress, compress_with_progress
from ilovepdf.security import validate_pdf_path

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
            for f in args.input_files:
                validate_pdf_path(f)
            merge_with_progress(args.input_files, args.output_path)
            print(f"Successfully merged into {args.output_path}")
        elif args.command == "split":
            validate_pdf_path(args.input_file)
            res = split_with_progress(args.input_file, args.output_dir)
            print(f"Successfully split into {len(res)} pages in {args.output_dir}")
        elif args.command == "compress":
            validate_pdf_path(args.input_file)
            compress_with_progress(args.input_file, args.output_path, quality=args.quality)
            print(f"Successfully compressed into {args.output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
