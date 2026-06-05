import re
from pathlib import Path
import fitz  # PyMuPDF

def clean_filename(name: str) -> str:
    """清理文件名中不允许的字符"""
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()

def split_pdf_to_pdf_and_md(input_pdf: str, output_dir: str, level: int = 1):
    """
    拆分PDF大章节并生成对应Markdown
    :param input_pdf: PDF文件路径
    :param output_dir: 输出目录
    :param level: 拆分的书签层级，王道大章节通常是 level=1
    """
    pdf_path = Path(input_pdf)
    if not pdf_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_pdf}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    toc = doc.get_toc()

    if not toc:
        raise ValueError("PDF中未发现书签目录")

    # 提取指定层级书签
    chapters = [
        (title, page - 1)  # fitz页码从0开始
        for lv, title, page in toc
        if lv == level
    ]

    if not chapters:
        raise ValueError(f"未发现 level={level} 的书签")

    print(f"发现 {len(chapters)} 个大章节\n")

    for idx, (title, start_page) in enumerate(chapters):
        # 寻找下一个同级章节
        if idx < len(chapters) - 1:
            end_page = chapters[idx + 1][1] - 1
        else:
            end_page = len(doc) - 1

        safe_title = clean_filename(title)
        pdf_outfile = output_path / f"{idx+1:02d}_{safe_title}.pdf"
        md_outfile = output_path / f"{idx+1:02d}_{safe_title}.md"

        print(f"[{idx+1:02d}] {safe_title} ({start_page+1}-{end_page+1}) 共 {end_page-start_page+1} 页")

        # --- 拆分 PDF ---
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
        new_doc.save(pdf_outfile, garbage=4, deflate=True)
        new_doc.close()

        # --- 生成 Markdown ---
        chapter_text = ""
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                chapter_text += text + "\n\n"

        # 添加一级标题
        chapter_md = f"# {title}\n\n{chapter_text.strip()}\n"
        md_outfile.write_text(chapter_md, encoding="utf-8")

    doc.close()
    print("\n拆分完成，PDF和Markdown已生成！")

if __name__ == "__main__":
    input_pdf = "数据结构.pdf"      # 你的PDF文件名
    output_dir = "output_chapters"  # 输出目录
    split_pdf_to_pdf_and_md(input_pdf, output_dir, level=1)