import os
import io
from PIL import Image
import PyPDF2
import img2pdf

def extract_images_from_pdf(pdf_path):
    images = []
    problem_pages = set()  # 用来记录有问题的页面
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
                                if stream:
                                    # 尝试打开图像
                                    image = Image.open(io.BytesIO(stream))
                                    images.append(image)
                                    print(f"Found and processed image on page {page_num}")
                                else:
                                    print(f"Empty stream on page {page_num}")
                                    problem_pages.add(page_num)
                            except Exception as e:
                                print(f"Error processing image on page {page_num}: {e}")
                                problem_pages.add(page_num)
    return images, problem_pages

def compress_images(images, quality_level):
    compressed_images = []
    for image in images:
        output = io.BytesIO()
        image.save(output, format="JPEG", optimize=True, quality=quality_level)
        compressed_images.append(output.getvalue())
    return compressed_images

def create_compressed_pdf(input_pdf, output_pdf, quality_level):
    images, problem_pages = extract_images_from_pdf(input_pdf)
    if not images and not problem_pages:
        print("No valid images found in the PDF.")
        return

    compressed_images = compress_images(images, quality_level)

    with open(input_pdf, 'rb') as original_file, open(output_pdf, "wb") as new_file:
        writer = PyPDF2.PdfWriter()

        # 从原始PDF中读取所有页面
        original_reader = PyPDF2.PdfReader(original_file)
        for page_num, page in enumerate(original_reader.pages):
            if page_num not in problem_pages:
                # 如果当前页面没有问题，则尝试用压缩后的图像替换页面上的图像
                resources = page.get("/Resources", None)
                if resources is not None:
                    resources = resources.get_object()
                    if "/XObject" in resources:
                        xobjects = resources["/XObject"]
                        new_xobjects = {}
                        for name, obj in xobjects.items():
                            if isinstance(obj, PyPDF2.generic.IndirectObject):
                                obj = obj.get_object()
                            if "/Subtype" in obj and obj["/Subtype"] == "/Image":
                                # 替换图像数据
                                new_xobjects[name] = PyPDF2.generic.StreamObject()
                                new_xobjects[name]._data = compressed_images.pop(0)
                            else:
                                new_xobjects[name] = obj
                        xobjects.update(new_xobjects)
                writer.add_page(page)
            else:
                # 如果页面有问题，则直接添加原始页面
                writer.add_page(page)

        writer.write(new_file)
    print(f"Compressed PDF has been saved to {output_pdf}")

if __name__ == "__main__":
    print("https://github.com/Ziyang-Bai/PDwarF")
    print("LJNT.XYZ")
    print("-----------")
    input_pdf = "input.pdf"
    output_pdf = "output.pdf"
    quality_levels = [25, 50, 75, 90, 95]
    quality_level = quality_levels[2]
    input_pdf = input("input pdf:")
    output_pdf = input("output pdf:")
    if not os.path.exists(input_pdf):
        print(f"The input PDF '{input_pdf}' does not exist.")
    else:
        create_compressed_pdf(input_pdf, output_pdf, quality_level)