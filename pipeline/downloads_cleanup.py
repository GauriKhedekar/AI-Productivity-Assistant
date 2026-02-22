import shutil
from pathlib import Path
from typing import Optional
from PIL import Image
import pytesseract
import pdfplumber
import docx

# -----------------------------
# KEYWORDS FOR COLLEGE DOCS
# -----------------------------
COLLEGE_DOC_KEYWORDS = {
    "Certificates": ["certificate", "degree", "marksheet", "transcript", "award", "completion"],
    "Important_College_Docs": ["card", "attendance", "affidavit", "domicile", "admission", "offer", "form", "fee", "receipt", "registration", "important doc", "bank", "account", "scholarship", "Loan", "result"]
}

# -----------------------------
# EXTRACT TEXT FROM FILE
# -----------------------------
def extract_text_from_file(file_path: Path) -> str:
    try:
        if file_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            return pytesseract.image_to_string(Image.open(file_path)).strip()
        elif file_path.suffix.lower() == ".pdf":
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages[:2]:
                    text += page.extract_text() or ""
            return text.strip()
        elif file_path.suffix.lower() == ".docx":
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs[:10]]).strip()
        elif file_path.suffix.lower() == ".txt":
            return file_path.read_text(encoding="utf-8", errors="ignore").strip()
        else:
            return ""
    except:
        return ""

# -----------------------------
# CLASSIFY COLLEGE FILE
# -----------------------------
def classify_college_file(text: str, filename: str) -> str:
    combined = (text + " " + filename).lower()
    for folder, keywords in COLLEGE_DOC_KEYWORDS.items():
        if any(k in combined for k in keywords):
            return folder
    return ""  # leave file in Downloads if it doesn't match

# -----------------------------
# GENERATE FILE NAME
# -----------------------------
def generate_filename(text: str, suffix: str) -> str:
    words = [w for w in text.replace("\n", " ").split() if w.isalnum()]
    if not words:
        return ""  # will fallback to original name
    return f"{'_'.join(words[:7])}{suffix.lower()}"

# -----------------------------
# MAIN CLEANUP FUNCTION
# -----------------------------
def cleanup_downloads(downloads_path: Optional[Path] = None) -> int:
    if downloads_path is None:
        downloads_path = Path.home() / "Downloads"

    # Ensure folders exist
    for folder in COLLEGE_DOC_KEYWORDS.keys():
        (downloads_path / folder).mkdir(exist_ok=True)

    organized_count = 0

    for file_path in downloads_path.iterdir():
        if not file_path.is_file():
            continue

        text = extract_text_from_file(file_path)
        folder_name = classify_college_file(text, file_path.name)

        # Skip files that don't match any folder
        if not folder_name:
            continue

        target_folder = downloads_path / folder_name

        # Only rename if OCR/text extraction succeeded
        new_name = generate_filename(text, file_path.suffix) or file_path.name
        new_file_path = target_folder / new_name

        # Avoid duplicates
        counter = 1
        while new_file_path.exists():
            stem = new_file_path.stem
            suff = new_file_path.suffix
            new_file_path = target_folder / f"{stem}_{counter}{suff}"
            counter += 1

        try:
            shutil.move(str(file_path), str(new_file_path))
            print(f"Moved {file_path.name} -> {folder_name}/{new_file_path.name}")
            organized_count += 1
        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")

    return organized_count
