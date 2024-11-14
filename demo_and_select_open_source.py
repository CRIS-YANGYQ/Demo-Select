"""
File: demo_and_select.py

Description:
This script processes images from a specified directory, groups them by template names, and generates HTML files to visualize the images. Each HTML file contains a table that displays images grouped by their templates. Users can select images using checkboxes, and save the selected images to a text file. The script supports batch processing, creating multiple HTML files if the number of images exceeds a specified threshold.

Functions:
1. `read_src_img(folder_path)`:
   - Reads images from the given folder and organizes them into groups based on their template names.
   - Returns a dictionary with template names as keys and lists of image file paths as values.

2. `resize_image(image, size)`:
   - Resizes the given image to the specified size using LANCZOS resampling.
   - Returns the resized image.

3. `read_leaf_img(folder_path)`:
   - Reads images from the given folder and organizes them into groups based on their leaf names.
   - Returns a dictionary with leaf names as keys and lists of image file paths as values.

4. `generate_html_with_templates(image_groups, src_group, index, demo_dir_path)`:
   - Generates HTML content to display images and their templates.
   - Includes interactive features for image selection and saving.
   - Returns the generated HTML content as a string.

5. `visualize_scratch_in_root(folder_path, src_group, output_dir, demo_lines=25)`:
   - Processes images in subfolders of the given directory, grouping them by template names.
   - Generates and saves HTML files to the specified output directory, with each file containing a batch of images based on the specified number of templates per file.

Usage:
1. Set the `src_folder_path` to the directory containing the images.
2. Set the `root_dir_path` to the directory where images are organized.
3. Set the `demo_dir_path` to the output directory for the HTML files.
4. Run the script to generate HTML files with the visualized images.

Example:
    src_folder_path = '/path/to/image/folder'
    leaf_dir_path = '/path/to/image/groups'
    demo_dir_path = '/path/to/output/html'
    lines_per_file = 25

    src_group = read_src_img(src_folder_path)
    leaf_group = read_leaf_img(leaf_dir_path)
    visualize_scratch_in_root(leaf_group, src_group, demo_dir_path, lines_per_file)

Attention:
# customized keyword can guide you customize the code to fit your own data structure and file name.


文件：demo_and_select.py

描述：
该脚本处理来自指定目录的图像，按模板名称对图像进行分组，并生成HTML文件以可视化图像。用户可在HTML文件中选择图片，并在浏览器内下载该图片的绝对路径到文本文件。
每个HTML文件包含一个表格，显示按模板分组的图像。用户可以使用复选框选择图像，并将所选图像保存到文本文件中。脚本支持批量处理，当Group数量超过指定阈值lines_per_file时，会生成多个HTML文件。

功能：
1. `read_src_img(folder_path)`：
   - 从给定的文件夹中读取图像，并根据模板名称将其组织成组。
   - 返回一个字典，以模板名称为键，以图像文件路径的列表为值。

2. `resize_image(image, size)`：
   - 使用LANCZOS重采样将给定图像调整为指定的大小。
   - 返回调整大小后的图像。

3. `read_leaf_img(folder_path)`：
   - 从给定的文件夹中读取图像，并根据叶子名称将其组织成组。
   - 返回一个字典，以叶子名称为键，以图像文件路径的列表为值。

4. `generate_html_with_templates(image_groups, src_group, index, demo_dir_path)`：
   - 生成HTML内容以显示图像及其模板。
   - 包含图像选择和保存的交互功能。
   - 返回生成的HTML内容（字符串格式）。

5. `visualize_scratch_in_root(folder_path, src_group, output_dir, demo_lines=25)`：
   - 处理给定目录的子文件夹中的图像，并按模板名称将其分组。
   - 生成并保存HTML文件到指定的输出目录，每个文件包含一批图像，基于指定的每个文件模板数。

使用方法：
1. 设置 `src_folder_path` 为包含图像的目录路径。
2. 设置 `root_dir_path` 为组织图像的目录路径。
3. 设置 `demo_dir_path` 为输出HTML文件的目录路径。
4. 运行脚本生成带有可视化图像的HTML文件。

示例：
```python
src_folder_path = '/path/to/image/folder'
leaf_dir_path = '/path/to/image/groups'
demo_dir_path = '/path/to/output/html'
lines_per_file = 25

src_group = read_src_img(src_folder_path)
leaf_group = read_leaf_img(leaf_dir_path)
visualize_scratch_in_root(leaf_group, src_group, demo_dir_path, lines_per_file)
```

注意:
# customized 关键字样可以引导你自定义代码以适应你的数据结构和文件名。
"""


import os
import re
import json
from PIL import Image

def read_src_img(folder_path):
    """
    Reads images from the specified folder and groups them by their template names.
    
    Parameters:
        folder_path (str): The path to the folder containing the images.
        
    Returns:
        dict: A dictionary where keys are template names and values are lists of image file paths.
    """
    if folder_path is None or not os.path.exists(folder_path):
        return {}
    image_groups = {}
    # Traverse the directory and collect images
    for filename in os.listdir(folder_path):
        if not filename.startswith("origin_"):
            continue
        # 可改：根据文件名或者路径划分可视化的组别
        # 这里假设文件名以"origin_"开头，后面跟着模板名，如"origin_1.jpg"
        # image_groups = {"1": "/origin_1_1.jpg" ,...}
        # To be customized: Group images dict are classified based on file names or paths
        # Here, we assume that the file name starts with "origin_" and followed by the template name, such as "origin_1.jpg"

        parts = os.path.splitext(filename)[0].split('_')
        if len(parts) != 2:# customized
            print(f"Error: File name {filename} is not in the correct format.")
            continue

        template = parts[1] # customized
        file_path = os.path.join(folder_path, filename)
        if template not in image_groups:
            image_groups[template] = []
        image_groups[template].append(file_path)
    return image_groups

def read_leaf_img(folder_path):
    """
    Reads images from the specified folder and groups them by their template names.
    
    Parameters:
        folder_path (str): The path to the folder containing the images.
        
    Returns:
        dict: A dictionary where keys are template names and values are lists of image file paths.
    """
    # Collect all image paths
    image_groups = {}
    
    # Traverse the folder
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(subfolder_path) or not subfolder.startswith("origin_"):
            continue
        for filename in os.listdir(subfolder_path):
            if not filename.startswith("origin_"):
                continue
            parts = filename.split('_')
            if len(parts) < 3: # customized
                print(f"Error: File name {filename} is not in the correct format.")
                continue
            template = parts[1] # customized
            file_path = os.path.join(subfolder_path, filename)
            if template not in image_groups:
                image_groups[template] = []
            image_groups[template].append(file_path)
    return image_groups

def resize_image(image, size):
    # 可视化图片前先缩放，否则可视化效果不好
    """
    Resizes the given image to the specified size using LANCZOS resampling.
    
    Parameters:
        image (PIL.Image): The image to be resized.
        size (tuple): The desired size as a (width, height) tuple.
        
    Returns:
        PIL.Image: The resized image.
    """
    return image.resize(size, Image.Resampling.LANCZOS)

def generate_html_with_templates(image_groups, src_group, index, demo_dir_path):
    """
    Generates HTML content for displaying images and their templates.
    
    Parameters:
        image_groups (dict): A dictionary of grouped images by their templates.
        src_group (dict): A dictionary of source images grouped by their templates.
        index (int): The index of the current batch of images.
        demo_dir_path (str): The directory path where the HTML file will be saved.
        
    Returns:
        str: The generated HTML content.
    """
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Gallery</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }}
            th, td {{
                border: 1px solid black;
                padding: 7px;
                text-align: center;
            }}
            img {{
                max-width: 200px;
                max-height: 200px;
                margin: 5px;
                cursor: pointer;
            }}
            .checkbox-container {{
                display: inline-block;
                align-items: center;
                cursor: pointer;
                position: relative;
                border: 2px solid transparent; /* 默认边框透明 */
            }}
            .checkbox-container input {{
                margin-right: 5px;
            }}
            .checkbox-container input:checked + img {{
                border: 2px solid red; /* 选中时边框为红色 */
            }}
            .selection-box {{
                border: 1px dashed #000;
                position: absolute;
                z-index: 1000;
                background: rgba(0, 0, 0, 0.1);
            }}
            .top-right-button {{
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }}
            .top-left-button {{
                position: fixed;
                top: 10px;
                left: 10px;
                padding: 10px 20px;
                background-color: red;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }}
            .src-image {{
                width: 800px;
                height: 800px;
                margin: 5px;
                cursor: pointer;
            }}
            .highlight {{
                border: 2px solid red; /* 高亮时边框为红色 */
            }}
        </style>
        <script>
            let isSelecting = false;
            let startX, startY;
            let selectionBox;
            let checkboxes = [];

            document.addEventListener('DOMContentLoaded', (event) => {{
                const containers = document.querySelectorAll('.checkbox-container');

                containers.forEach(container => {{
                    container.addEventListener('click', (e) => {{
                        if (!isSelecting) {{
                            toggleCheckbox(container);
                        }}
                    }});
                }});

                document.addEventListener('mousedown', (e) => {{
                    if (e.target.classList.contains('checkbox-container') || e.target.closest('.checkbox-container')) {{
                        isSelecting = true;
                        startX = e.pageX;
                        startY = e.pageY;
                        selectionBox = document.createElement('div');
                        selectionBox.className = 'selection-box';
                        selectionBox.style.left = startX + 'px';
                        selectionBox.style.top = startY + 'px';
                        document.body.appendChild(selectionBox);
                        checkboxes = Array.from(containers).map(container => container.querySelector('input[type="checkbox"]'));
                    }}
                }});

                document.addEventListener('mousemove', (e) => {{
                    if (isSelecting) {{
                        const currentX = e.pageX;
                        const currentY = e.pageY;
                        const width = Math.abs(currentX - startX);
                        const height = Math.abs(currentY - startY);
                        selectionBox.style.width = width + 'px';
                        selectionBox.style.height = height + 'px';
                        selectionBox.style.left = Math.min(startX, currentX) + 'px';
                        selectionBox.style.top = Math.min(startY, currentY) + 'px';
                    }}
                }});

                document.addEventListener('mouseup', (e) => {{
                    if (isSelecting) {{
                        isSelecting = false;
                        const rect = selectionBox.getBoundingClientRect();
                        checkboxes.forEach(checkbox => {{
                            const boxRect = checkbox.closest('.checkbox-container').getBoundingClientRect();
                            if (
                                boxRect.left < rect.right &&
                                boxRect.right > rect.left &&
                                boxRect.top < rect.bottom &&
                                boxRect.bottom > rect.top
                            ) {{
                                checkbox.checked = !checkbox.checked;
                                updateCheckboxStyle(checkbox);
                            }}
                        }});
                        selectionBox.parentNode.removeChild(selectionBox);
                    }}
                }});

                document.getElementById('save-button').addEventListener('click', saveSelectedImages);
                document.getElementById('load-button').addEventListener('click', loadSelectedTxt);

                document.addEventListener('keydown', (e) => {{
                    if (e.ctrlKey && e.key === 's') {{
                        e.preventDefault();
                        saveSelectedImages();
                    }}
                    if (e.ctrlKey && e.key === 'l') {{
                        e.preventDefault();
                        loadSelectedTxt();
                    }}
                }});
            }});

            function toggleCheckbox(container) {{
                const checkbox = container.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                updateCheckboxStyle(checkbox);
            }}

            function updateCheckboxStyle(checkbox) {{
                const container = checkbox.closest('.checkbox-container');
                if (checkbox.checked) {{
                    container.style.border = '2px solid red';
                }} else {{
                    container.style.border = '2px solid transparent';
                }}
            }}


            function saveSelectedImages() {{
                const selectedImages = [];
                const checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]:checked');
                checkboxes.forEach(checkbox => {{
                    const img = checkbox.nextElementSibling;
                    const imgUrl = img.src;

                    // 获取当前页面的基本 URL (协议 + 主机名 + 端口号)
                    const baseUrl = window.location.origin;

                    // 使用 baseUrl 来计算相对路径
                    const relativePath = imgUrl.replace(baseUrl + '/', '');

                    selectedImages.push(relativePath);
                }});


                const blob = new Blob([selectedImages.join('\\n')], {{ type: 'text/plain' }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'selected_images_{index}.txt';
                document.body.appendChild(a);
                a.click();
                URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }}

            function loadSelectedTxt() {{
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = '.txt';
                input.addEventListener('change', (e) => {{
                    const file = e.target.files[0];
                    if (file) {{
                        const reader = new FileReader();
                        reader.onload = function(event) {{
                            const lines = event.target.result.split('\\n');
                            const containers = document.querySelectorAll('.checkbox-container');
                            containers.forEach(container => {{
                                const img = container.querySelector('img');
                                const imgSrc = img.src;
                                const imgName = imgSrc.substring(imgSrc.lastIndexOf('/') + 1);
                                
                                lines.forEach(line => {{
                                    const lineName = line.substring(line.lastIndexOf('/') + 1);
                                    if (imgName === lineName) {{
                                        const checkbox = container.querySelector('input[type="checkbox"]');
                                        checkbox.checked = true;
                                        updateCheckboxStyle(checkbox);
                                    }}
                                }});
                            }});
                        }};
                        reader.readAsText(file);
                    }}
                }});
                input.click();
            }}
        </script>
    </head>
    <body>
        <button id="save-button" class="top-right-button">Save Selected Images</button>
        <button id="load-button" class="top-left-button">Load Selected Info</button>
        <table>
            <tr>
                <th>Template</th>
                <th>Images</th>
                <th>Source Images</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    rows = ""
    cur_path = demo_dir_path
    for template, images in image_groups.items():
        row = f"<tr><td>{template}</td><td>"
        for image_path in images:
            # 存放图片相对于可视化HTML的相对路径
            rel_path = os.path.relpath(image_path, cur_path)
            row += f"""
            <div class="checkbox-container" onclick="toggleCheckbox(this);">
                <input type="checkbox">
                <img src="{rel_path}" alt="{template}">
            </div>
            """
        row += "</td><td>"
        for src_image in src_group.get(template, []):
            rel_path = os.path.relpath(src_image, cur_path)
            row += f'<img src="{rel_path}" alt="source_image" class="src-image">'
        row += "</td></tr>"
        rows += row

    return html_template.format(index=index, rows=rows)



def visualize_scratch_in_root(leaf_group, src_group, output_dir, demo_lines=25):
    """
    Visualizes images in the specified folder by grouping them, generating HTML files, and saving them to the output directory.
    
    Parameters:
        folder_path (str): The path to the folder containing subfolders with images.
        src_group (dict): A dictionary of source images grouped by their templates.
        output_dir (str): The directory where the generated HTML files will be saved.
        demo_lines (int): The number of templates to include per HTML file.
    """

    os.makedirs(output_dir, exist_ok=True)

    # Custom sorting function, sort by numerical value
    def sort_key(template):
        match = re.match(r"(\d+)", template)
        return int(match.group(1)) if match else float('inf')
    
    # Sort templates by numerical value
    templates = sorted(leaf_group.keys(), key=sort_key)
    for identifier, img_path_lst in leaf_group.items():
        leaf_group[identifier] = sorted(img_path_lst)
    
    for i in range(0, len(templates), demo_lines):
        # Generate HTML file name
        start = i // demo_lines
        output_file = f'demo_batch_{start + 1}.html'

        batch_templates = templates[i:i + demo_lines]
        batch_image_groups = {tpl: leaf_group[tpl] for tpl in batch_templates}
        html_content = generate_html_with_templates(batch_image_groups, src_group, "batch_" + str(start+1), output_dir)
        
        # Save HTML file
        with open(os.path.join(output_dir, output_file), 'w') as file:
            file.write(html_content)
        
        print(f"HTML file has been created at {os.path.join(output_dir, output_file)}")

if __name__ == "__main__":
    # In this case, one image and some similar images can seen as a group. Their filenames can indicate their relationship uniquely.
    # 本代码解决的是，一张图片与多张图片有对应关系，需要检查并删去多张图片中的不合格图片，常用于手动筛选爬取后的不良图片。 HTML最后会给出你框选的图片路径txt
    """
    1. Click the frame/button of your targer images, and then click the red button on the top right to [Save Selected Images]/[ctrl + s] to save the selected images' path txt file.
    You will find a txt file downloaded in your device, which contains the selected images paths.
    2. Load the selected txt file by clicking the red button on the top left to [Load Selected Info]/[ctrl + d].
    1. 保存：勾选框，点击图片或者左键框选需要删除的图片，在确认勾选图片正确之后，点击右上角绿色按钮[Save Selected Images]/[ctrl + s],即可保存该demo文件的目标图片路径txt。
    2. 载入：导入selected_txt，检查选择的图片质量，点击左上角红色按钮[Load Selected Info]/[ctrl + d]
    """
    # Image selected from source folder
    # src_folder_path can be none, and source column will be empty in the HTML file
    src_folder_path = 'data/src'
    src_group = read_src_img(src_folder_path)

    # Image selected from leaf folder
    leaf_dir_path = "data/leaf"
    leaf_group = read_leaf_img(leaf_dir_path)

    # Optional: Check the source and leaf image groups
    with open("json/leaf_group.json", "w") as f:
        json.dump(leaf_group, f, indent=4)
    with open("json/src_group.json", "w") as f:
        json.dump(src_group, f, indent=4)

    # Number of groups in one demo file. The number depends on your device and the average number of images per group.
    # If lines are too large, make sure your device is capable of R/W lots of images
    lines_per_file = 25  # default


    # demo directory
    demo_dir_path = "html"
    visualize_scratch_in_root(leaf_group, src_group, demo_dir_path, lines_per_file)
