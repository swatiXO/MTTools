import os
from django.shortcuts import render, redirect
from main.forms import DocumentForm
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from pdf2image import convert_from_path
import pytesseract
from django.http import JsonResponse
from docx import Document as DocxDocument
from tempfile import TemporaryDirectory
from django.http import StreamingHttpResponse
from concurrent.futures import ThreadPoolExecutor
import time

extracted_text = None


def extract_text_from_file(file_path):
    start_time = time.time()
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    print(f"\n🚀 Starting extraction for: {file_path}")
    print(f"📄 File type: {ext}")

    if ext == ".pdf":
        try:
            pdf_start = time.time()
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            print(f"📘 Total pages: {total_pages}")

            with TemporaryDirectory() as tempdir:
                def process_page(i):
                    """Extract or OCR a single page."""
                    page_start = time.time()
                    try:
                        page = reader.pages[i - 1]
                        page_text = page.extract_text()

                        if not page_text or len(page_text.strip()) < 30:
                            print(f"🕵️ Page {i}: Using OCR fallback...")
                            images = convert_from_path(
                                file_path, first_page=i, last_page=i, output_folder=tempdir
                            )
                            if images:
                                ocr_start = time.time()
                                ocr_text = pytesseract.image_to_string(images[0], lang="eng")
                                ocr_time = time.time() - ocr_start
                                print(f"⏱️ OCR for page {i} took {ocr_time:.2f}s")
                                result = f"\n{ocr_text}\n"
                            else:
                                result = ""
                        else:
                            result = f"\n{page_text}\n"

                        page_time = time.time() - page_start
                        print(f"✅ Page {i} processed in {page_time:.2f}s")
                        return result

                    except Exception as err:
                        print(f"⚠️ Error on page {i}: {err}")
                        return ""

                # ⚡ Run in parallel threads
                with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                    results = list(executor.map(process_page, range(1, total_pages + 1)))

            text = "".join(results)
            pdf_time = time.time() - pdf_start
            print(f"✅ PDF extraction complete in {pdf_time:.2f}s (optimized).")

        except Exception as e:
            print(f"⚠️ PDF extraction error: {e}")
            text = "[Unable to extract text from PDF]"

    elif ext == ".docx":
        docx_start = time.time()
        try:
            doc = DocxDocument(file_path)
            text = "\n".join(para.text for para in doc.paragraphs)
            print(f"✅ DOCX extracted in {time.time() - docx_start:.2f}s")
        except Exception as e:
            print(f"⚠️ DOCX extraction error: {e}")
            text = "[Unable to extract text from document]"

    elif ext == ".txt":
        txt_start = time.time()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            print(f"✅ TXT read in {time.time() - txt_start:.2f}s")
        except Exception as e:
            print(f"⚠️ TXT extraction error: {e}")
            text = "[Unable to read text file]"

    else:
        text = "Unsupported file type."

    total_time = time.time() - start_time
    print(f"🏁 Total extraction time: {total_time:.2f}s\n")

    return text.strip()
import uuid
from .embeddings import EmbeddingManager
from main.models import Document
EXECUTOR = ThreadPoolExecutor(max_workers=8)
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"success": False, "error": "Invalid form."}, status=400)

            # Save Document Instance
        doc = form.save(commit=False)
        if not getattr(doc,"storage_key",None):
            doc.storage_key = uuid.uuid4().hex
        doc.save()
        extracted_text = extract_text_from_file(doc.file.path)
        request.session['extracted_text'] = extracted_text[:100000]
        request.session['docId']=doc.id
        # print("✅ Extracted Text:", extracted_text[:500])  # print preview only, not full text
        

            # Launch background FAISS/index build so user doesn't wait
        def build_index_and_update(doc_id, text):
            try:
                manager = EmbeddingManager(storage_key=Document.objects.get(id=doc_id).storage_key)
                manager.build_index(text)
                # update num_chunks if you persist it in model
                num_chunks = len(manager.chunks or [])
                Document.objects.filter(id=doc_id).update(num_chunks=num_chunks)
            except Exception as e:
                # log the error using your logging system
                print("Error building embeddings:", e)
        EXECUTOR.submit(build_index_and_update, doc.id, extracted_text)

        # Respond immediately
        return JsonResponse({
            "success": True,
            "doc_id": doc.id,
            "title": doc.title,
            "extracted_text": extracted_text  # optional, used by your existing preview flow
        })
    form = DocumentForm()
    return render(request, 'documents/upload.html', {'form': form})
