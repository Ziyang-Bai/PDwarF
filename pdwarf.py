import pikepdf
from PIL import Image
import io

def compress_pdf(input_path, output_path, compression_level=3):
    """
    压缩PDF文件。
    
    :param input_path: 输入PDF文件路径
    :param output_path: 输出PDF文件路径
    :param compression_level: 压缩级别，0-最低压缩，4-最高压缩
    """
    # 打开原始PDF文件
    with pikepdf.open(input_path) as pdf:
        new_pdf = pikepdf.Pdf.new()

        for page in pdf.pages:
            resources = page.Resources
            xobjects = resources.XObject
            new_xobjects = pikepdf.Dictionary()
            
            for name, xobj in xobjects.items():
                if xobj.Type == '/XObject' and xobj.Subtype == '/Image':
                    # 读取图像数据
                    img_data = xobj.stream.get_data()
                    image = Image.open(io.BytesIO(img_data))
                    
                    # 根据压缩级别调整图像质量
                    quality = 95 - (compression_level * 10)
                    new_img_data = io.BytesIO()
                    image.save(new_img_data, format='JPEG', quality=quality)
                    
                    # 创建一个新的流对象，并设置压缩后的图像数据
                    stream = pikepdf.Stream(new_pdf, new_img_data.getvalue())
                    new_xobjects[name] = xobj.copy_with_new_stream(stream)
                else:
                    new_xobjects[name] = xobj
                    
            resources.XObject = new_xobjects
            new_page = pikepdf.Page(pdf, page_index=page.Index)
            new_pdf.pages.append(new_page)

        # 写入新PDF文件
        new_pdf.save(output_path)

# 使用示例
compress_pdf('input.pdf', 'output.pdf', compression_level=3)