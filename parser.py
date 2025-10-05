import fitz  
import re
from models import Standard, Section
from sqlalchemy.orm import Session

SECTION_PATTERN = re.compile(r"^\d+(\.\d+)*\s+.+")  

def parse_standard_pdf(file_path: str, db: Session, standard_name: str, version: str = None, start_page: int = 0):
    """
    Parse a standard PDF file starting from a specific page number.

    Args:
        file_path (str): Path to the PDF file.
        db (Session): SQLAlchemy database session.
        standard_name (str): Name of the standard.
        version (str, optional): Version or edition of the standard.
        start_page (int, optional): Page number to start parsing from (0-indexed).
    """
    doc = fitz.open(file_path)
    total_pages = len(doc)

    if start_page >= total_pages:
        raise ValueError(f"start_page {start_page} is beyond the total number of pages ({total_pages}).")

    all_text = ""
    for page_num in range(start_page, total_pages):
        page = doc[page_num]
        all_text += page.get_text("text")

    
    lines = all_text.split("\n")
    current_section = None
    current_text = []

    
    standard = Standard(name=standard_name, version=version, file_path=file_path)
    db.add(standard)
    db.commit()

    for line in lines:
        stripped = line.strip()
        if SECTION_PATTERN.match(stripped):
            
            if current_section:
                section = Section(
                    standard_id=standard.id,
                    section_number=current_section.split(" ")[0],
                    title=" ".join(current_section.split(" ")[1:]),
                    content="\n".join(current_text),
                )
                db.add(section)
                db.commit()
                current_text = []
            current_section = stripped
        else:
            current_text.append(stripped)

    
    if current_section:
        section = Section(
            standard_id=standard.id,
            section_number=current_section.split(" ")[0],
            title=" ".join(current_section.split(" ")[1:]),
            content="\n".join(current_text),
        )
        db.add(section)
        db.commit()

    print(f"✅ Parsed and stored '{standard_name}' starting from page {start_page + 1}")
