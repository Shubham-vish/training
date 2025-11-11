#!/usr/bin/env python3
"""
FIXED PDF generator - simplified CSS for wkhtmltopdf compatibility
Supports command-line arguments for input/output file paths
"""

import markdown
import pdfkit
import re
import base64
import requests
import os
from datetime import datetime
import shutil
import argparse


# Default file paths
DEFAULT_MD_FILE = "presentation/diagrams/mermaid_diagrams.md"
DEFAULT_PDF_FILE = "Interview_Kickstart_Multi_Agent_Demo.pdf"
    
    
def get_mermaid_image(diagram_content, diagram_num, output_dir):
    """Get an ultra high-quality Mermaid diagram image using mermaid.ink with natural aspect ratio"""
    
    try:
        print(f"📡 Getting Ultra-HQ diagram {diagram_num}...")
        
        # Determine optimal WIDTH based on diagram type (let height be natural)
        # Detect diagram complexity for better sizing
        is_mindmap = 'mindmap' in diagram_content
        is_flowchart = 'flowchart' in diagram_content or 'graph' in diagram_content
        has_many_nodes = diagram_content.count('[') > 15  # Complex diagram
        
        # Adaptive width only - let mermaid.ink determine natural height
        if is_mindmap:
            width = 2400  # Mind maps need more space
        elif has_many_nodes:
            width = 2200  # Complex diagrams need maximum width
        elif is_flowchart:
            width = 2000  # Flowcharts 
        else:
            width = 1800  # Standard diagrams
        
        # Enhanced diagram with better contrast configuration
        enhanced_content = f"""%%{{init: {{
  'theme': 'base',
  'themeVariables': {{
    'primaryColor': '#ffffff',
    'primaryTextColor': '#000000',
    'primaryBorderColor': '#333333',
    'lineColor': '#333333',
    'secondaryColor': '#f9f9f9',
    'tertiaryColor': '#ffffff',
    'background': '#ffffff',
    'mainBkg': '#ffffff',
    'secondBkg': '#f5f5f5',
    'tertiaryBkg': '#ffffff',
    'textColor': '#000000',
    'fontWeight': 'bold'
  }},
  'fontFamily': 'Arial, Helvetica, sans-serif',
  'fontSize': 16,
  'fontWeight': 'bold'
}}}}%%
{diagram_content}"""

        # Special handling for mind maps
        if is_mindmap:
            enhanced_content = f"""%%{{init: {{
  'mindmap': {{
    'theme': 'default'
  }}
}}}}%%
{diagram_content}"""
        
        # Encode for mermaid.ink - only specify width, let height be natural
        encoded_diagram = base64.urlsafe_b64encode(enhanced_content.encode('utf-8')).decode('ascii')
        img_url = f"https://mermaid.ink/img/{encoded_diagram}?type=png&width={width}&bgColor=white"
        
        response = requests.get(img_url, timeout=60)
        response.raise_for_status()
        
        # Save image to file
        img_filename = f"diagram_{diagram_num:02d}.png"
        img_path = os.path.join(output_dir, img_filename)
        
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Got Ultra-HQ diagram {diagram_num} ({len(response.content):,} bytes, width={width}) → {img_filename}")
        
        # Convert to base64 for embedding
        img_base64 = base64.b64encode(response.content).decode('ascii')
        
        # Return with requested width (height will be natural/proportional)
        return img_base64, img_path, width, 0  # 0 for height means "natural"
        
    except Exception as e:
        print(f"❌ Failed to get diagram {diagram_num}: {str(e)}")
        # Fallback to simple version
        try:
            encoded_diagram = base64.urlsafe_b64encode(diagram_content.encode('utf-8')).decode('ascii')
            # Only specify width for fallback too
            img_url = f"https://mermaid.ink/img/{encoded_diagram}?type=png&width=3600"
            response = requests.get(img_url, timeout=30)
            response.raise_for_status()
            
            # Save fallback image to file
            img_filename = f"diagram_{diagram_num:02d}_fallback.png"
            img_path = os.path.join(output_dir, img_filename)
            
            with open(img_path, 'wb') as f:
                f.write(response.content)
            
            img_base64 = base64.b64encode(response.content).decode('ascii')
            print(f"✅ Got fallback diagram {diagram_num} (width=1800) → {img_filename}")
            return img_base64, img_path, 1800, 0  # 0 for height means "natural"
        except:
            return None, None, 0, 0

def main(md_file=None, pdf_file=None):
    """Generate PDF from markdown diagrams
    
    Args:
        md_file: Path to input markdown file (default: from DEFAULT_MD_FILE)
        pdf_file: Path to output PDF file (default: from DEFAULT_PDF_FILE)
    """
    
    # Use defaults if not provided
    if md_file is None:
        md_file = DEFAULT_MD_FILE
    if pdf_file is None:
        pdf_file = DEFAULT_PDF_FILE
    
    print("🎯 Creating High-Quality PDF for Interview Kickstart Demo...")
    print(f"📖 Input:  {md_file}")
    print(f"📄 Output: {pdf_file}")
    
    # Create timestamped output directory for images
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"generated_diagrams_{timestamp}"
    
    # Remove old generated_diagrams_* folders and create new one
    for item in os.listdir('.'):
        if item.startswith('generated_diagrams_') and os.path.isdir(item):
            print(f"🗑️  Removing old diagram folder: {item}")
            shutil.rmtree(item)
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Created fresh diagram folder: {output_dir}")
    
    # Read markdown
    print(f"📖 Reading: {md_file}")
    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Process content for better formatting
    print("🔄 Processing content for intelligent page layout...")
    
    # Simple processing - just ensure proper spacing
    content = content.replace('\n\n\n', '\n\n')  # Remove excessive line breaks
    
    # Intelligent page break insertion for better readability
    # Add page breaks before major sections that follow large diagrams
    lines = content.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        processed_lines.append(line)
        
        # Check if current line is end of mermaid diagram
        if line.strip() == '```' and i > 0:
            # Look back to see if this closes a mermaid block
            found_mermaid_start = False
            for j in range(i - 1, max(0, i - 50), -1):
                if lines[j].strip() == '```mermaid':
                    found_mermaid_start = True
                    break
            
            if found_mermaid_start:
                # Look ahead to see if there's a major heading soon (## but not ###)
                for j in range(i + 1, min(i + 8, len(lines))):
                    next_line = lines[j].strip()
                    # Check for ## heading (but not ###)
                    if next_line.startswith('## ') and not next_line.startswith('### '):
                        # Insert page break hint before the heading
                        # Add HTML comment to force page break
                        processed_lines.append('\n<div class="page-break-hint"></div>\n')
                        print(f"📄 Added intelligent page break before: {next_line[:50]}...")
                        break
        
        i += 1
    
    content = '\n'.join(processed_lines)
    
    diagram_count = 0
    saved_images = []
    
    def replace_mermaid(match):
        nonlocal diagram_count
        diagram_content = match.group(1).strip()
        diagram_count += 1
        
        # Get high-quality image with natural dimensions
        result = get_mermaid_image(diagram_content, diagram_count, output_dir)
        
        if result[0]:  # Check if img_base64 is not None
            img_base64, img_path, img_width, img_height = result
            saved_images.append(img_path)
            
            # Simple sizing based on diagram width request
            # Images will maintain their natural aspect ratio
            if img_width >= 2200:  # Large complex diagrams
                max_width = "95%"
            elif img_width >= 2000:  # Medium-large diagrams
                max_width = "90%"
            else:  # Standard diagrams
                max_width = "85%"
            
            # Use absolute file path for wkhtmltopdf
            abs_img_path = os.path.abspath(img_path)
            
            # CRITICAL: Only set max-width, let height be auto to preserve aspect ratio
            return f'''
<div class="diagram-container">
    <img src="{abs_img_path}" 
         style="max-width: {max_width}; max-height: 9in; width: auto; height: auto;"
         alt="Multi-Agent System Diagram {diagram_count}" />
</div>
'''
        else:
            return f"[Diagram {diagram_count} could not be loaded]"
    
    print("🔄 Processing Mermaid diagrams with enhanced quality...")
    
    # Replace all Mermaid blocks
    pattern = r'```mermaid\n(.*?)\n```'
    content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
    
    print("📝 Converting to HTML...")
    
    # Convert to HTML
    md = markdown.Markdown(extensions=['extra'])
    html_body = md.convert(content)
    
    # SIMPLIFIED HTML template with page break controls
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Multi-Agent Systems - Interview Kickstart Demo</title>
    <style>
        @page {{ 
            size: A4;
            margin: 0.4in;  /* Further reduced from 0.5in for more content space */
        }}
        
        body {{ 
            font-family: Arial, Helvetica, sans-serif; 
            line-height: 1.5; 
            color: #333; 
            font-size: 13px;
            margin: 0;
            padding: 0;
        }}
        
        h1 {{ 
            color: #2c3e50; 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 8px; 
            font-size: 22px;
            margin-top: 10px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }}
        
        h2 {{ 
            color: #34495e; 
            border-bottom: 2px solid #ecf0f1; 
            padding-bottom: 6px; 
            font-size: 18px;
            margin-top: 20px;
            margin-bottom: 12px;
            page-break-after: avoid;
            page-break-before: auto;
            orphans: 3;
            widows: 3;
        }}
        
        /* Start new page for headings if not enough space */
        h2:not(:first-of-type) {{
            page-break-before: auto;
        }}
        
        h3 {{ 
            color: #7f8c8d; 
            font-size: 16px;
            margin-top: 15px;
            margin-bottom: 10px;
            page-break-after: avoid;
            orphans: 2;
            widows: 2;
        }}
        
        /* Critical: Prevent images from breaking across pages */
        .diagram-container {{
            text-align: center;
            margin-top: 12px;
            margin-bottom: 20px;  /* Increased spacing after images */
            page-break-inside: avoid !important;
            page-break-before: auto;
            page-break-after: auto;
        }}
        
        /* Images with intelligent sizing - width set inline per diagram */
        img {{ 
            /* Width and max-height are set inline per diagram for optimal display */
            height: auto;
            border: 1px solid #bbb;
            border-radius: 4px;
            padding: 3px;
            display: block;
            margin: 0 auto;
            page-break-inside: avoid !important;
            background: white;
        }}
        
        /* Ensure proper spacing between image and next heading */
        .diagram-container + h2,
        .diagram-container + h3 {{
            margin-top: 25px;  /* Extra space after images before headings */
        }}
        
        /* Intelligent page break hints */
        .page-break-hint {{
            height: 0;
            margin: 0;
            padding: 0;
            page-break-before: always !important;
        }}
        
        /* Keep heading close to following content */
        h2 + p,
        h2 + ul,
        h2 + .diagram-container {{
            page-break-before: avoid;
        }}
        
        p {{ 
            margin: 8px 0; 
            orphans: 3;
            widows: 3;
        }}
        
        ul, ol {{ 
            margin: 8px 0; 
            padding-left: 20px;
            orphans: 2;
            widows: 2;
        }}
        
        li {{ margin: 4px 0; }}
        
        /* Table styling for markdown tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            font-size: 12px;
            page-break-inside: auto;
        }}
        
        thead {{
            background-color: #34495e;
            color: white;
            font-weight: bold;
        }}
        
        th {{
            padding: 10px 8px;
            text-align: left;
            border: 1px solid #ddd;
            background-color: #34495e;
            color: white;
            font-weight: bold;
        }}
        
        td {{
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        tbody tr:hover {{
            background-color: #f0f0f0;
        }}
        
        /* Prevent table headers from being orphaned */
        thead {{
            page-break-after: avoid;
        }}
        
        tr {{
            page-break-inside: avoid;
        }}
        
        code {{ 
            background: #f5f5f5; 
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 12px;
        }}
        
        /* Better content flow */
        strong {{
            page-break-after: avoid;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>'''
    
    print("📄 Creating high-quality PDF with embedded images...")
    
    # Options optimized for page breaks and margins
    options = {
        'page-size': 'A4',
        'margin-top': '0.4in',
        'margin-right': '0.4in',
        'margin-bottom': '0.4in',
        'margin-left': '0.4in',
        'enable-local-file-access': '',
        'encoding': 'UTF-8',
    }
    
    try:
        # Save HTML to file for better wkhtmltopdf compatibility
        html_file = "temp_content.html"
        debug_html_file = "debug_preview.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Also save debug version for manual review
        with open(debug_html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 Saved HTML to: {html_file}")
        print(f"🔍 Debug HTML saved to: {debug_html_file} (open in browser to verify)")
        
        # Generate PDF from HTML file
        pdfkit.from_file(html_file, pdf_file, options=options)
        
        # Clean up temp file (keep debug file)
        os.remove(html_file)
        
        # Check file size
        file_size = os.path.getsize(pdf_file)
        size_mb = file_size / (1024 * 1024)
        
        print(f"\n✅ PDF created: {pdf_file}")
        print(f"📏 Size: {size_mb:.1f} MB ({file_size:,} bytes)")
        
        # Calculate expected size (rough estimate)
        total_img_size = sum(os.path.getsize(img) for img in saved_images)
        expected_min_size = total_img_size * 0.8  # Allow some compression
        
        if file_size < expected_min_size:
            print(f"⚠️ WARNING: PDF size ({file_size:,} bytes) is smaller than expected")
            print(f"   Total image size: {total_img_size:,} bytes")
            print(f"   Images may not be embedded properly!")
        else:
            print(f"✅ Images appear to be embedded correctly!")
        
        if size_mb > 30:
            print("⚠️ Warning: File size exceeds 30MB limit")
        else:
            print("✅ Within 30MB limit")
        
        # Show saved images
        print(f"\n📸 Saved {len(saved_images)} diagram images to: {output_dir}/")
        for i, img_path in enumerate(saved_images, 1):
            img_size = os.path.getsize(img_path) / 1024  # KB
            print(f"   {i}. {os.path.basename(img_path)} ({img_size:.1f} KB)")
        
        print(f"\n🎉 SUCCESS! PDF ready: {pdf_file}")
        print(f"💡 Review individual diagrams in: {output_dir}/")
        print(f"🔍 Open {debug_html_file} in browser to verify image display")
        
    except Exception as e:
        print(f"❌ PDF creation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Generate PDF with embedded Mermaid diagrams from Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s
    Use default files
    
  %(prog)s -i my_doc.md
    Custom input, default output
    
  %(prog)s -i my_doc.md -o my_output.pdf
    Custom input and output
    
  %(prog)s --input docs/diagrams.md --output reports/final.pdf
    Full custom paths
        '''
    )
    
    parser.add_argument(
        '-i', '--input',
        dest='input_file',
        default=DEFAULT_MD_FILE,
        help=f'Input markdown file (default: {DEFAULT_MD_FILE})'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        default=DEFAULT_PDF_FILE,
        help=f'Output PDF file (default: {DEFAULT_PDF_FILE})'
    )
    
    args = parser.parse_args()
    
    # Run main with parsed arguments
    main(md_file=args.input_file, pdf_file=args.output_file)
