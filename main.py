# voc2yolo @rasvet
import os
import xml.etree.ElementTree as ET


def convert_voc_to_yolo(xml_file, txt_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    with open(txt_file, 'w') as f:
        for obj in root.findall('object'):
            class_id = 0

            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            x_center = ((xmin + xmax) / 2) / width
            y_center = ((ymin + ymax) / 2) / height
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height

            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")

def batch_convert(input_dir, output_dir, object_class):
    os.makedirs(output_dir, exist_ok=True)

    converted_count = 0
    for filename in os.listdir(input_dir):
        if filename.endswith('.xml'):
            xml_path = os.path.join(input_dir, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_dir, txt_filename)

            convert_voc_to_yolo(xml_path, txt_path)
            print(f"Конвертирован: {filename}")
            converted_count += 1

    classes_file = os.path.join(output_dir, 'classes.txt')
    with open(classes_file, 'w') as f:
        f.write(f'{object_class}\n')
    print(f"Создан файл: {classes_file}")

    print(f"Обработано файлов в {os.path.basename(input_dir)}: {converted_count}")
    return converted_count

def process_all_folders(input_root, output_root):
    subfolders = [f for f in os.listdir(input_root) if os.path.isdir(os.path.join(input_root, f))]

    total_files = 0

    for folder_name in subfolders:
        input_folder = os.path.join(input_root, folder_name, object_class)
        output_folder = os.path.join(output_root, folder_name)

        print(f"\n--- Обрабатывается папка: {folder_name} ---")
        files_count = batch_convert(input_folder, output_folder, object_class)
        total_files += files_count

    print(f"\n=== ВСЕГО ОБРАБОТАНО ФАЙЛОВ: {total_files} ===")

if __name__ == "__main__":
    object_class = 'monsters'
    input_directory = 'input'
    output_directory = 'output'

    process_all_folders(input_directory, output_directory, object_class)
    print("Все операции завершены!")
