import os
import io
from PIL import Image
import PyPDF2
import img2pdf

def extract_images_from_pdf(pdf_path):
    images = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            resources = page.get("/Resources", None)
            if resources is not None:
                resources = resources.get_object()
                if "/XObject" in resources:
                    xobjects = resources["/XObject"]
                    for obj in xobjects.values():
                        if isinstance(obj, PyPDF2.generic.IndirectObject):
                            obj = obj.get_object()
                        if "/Subtype" in obj and obj["/Subtype"] == "/Image":
                            try:
                                # 获取图像数据
                                stream = obj._data
                                # 检查流是否为空
                                if stream:
                                    # 尝试打开图像
                                    image = Image.open(io.BytesIO(stream))
                                    images.append(image)
                                    print(f"Found and processed image on page {page_num}")
                                else:
                                    print(f"Empty stream on page {page_num}")
                            except Exception as e:
                                print(f"Error processing image on page {page_num}: {e}")
    return images

def compress_images(images, quality_level):
    compressed_images = []
    for image in images:
        output = io.BytesIO()
        image.save(output, format="JPEG", optimize=True, quality=quality_level)
        compressed_images.append(output.getvalue())
    return compressed_images

def create_compressed_pdf(input_pdf, output_pdf, quality_level):
    images = extract_images_from_pdf(input_pdf)
    if not images:
        print("No valid images found in the PDF.")
        return
    
    compressed_images = compress_images(images, quality_level)
    
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(compressed_images))
    print(f"Compressed PDF has been saved to {output_pdf}")

if __name__ == "__main__":
    input_pdf = "input.pdf"
    output_pdf = "output.pdf"
    quality_levels = [25, 50, 75, 90, 95]  # 压缩等级
    quality_level = quality_levels[2]  # 选择第三个等级

    if not os.path.exists(input_pdf):
        print(f"The input PDF '{input_pdf}' does not exist.")
    else:
        create_compressed_pdf(input_pdf, output_pdf, quality_level)