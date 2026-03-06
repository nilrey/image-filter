import argparse
import sys
from pathlib import Path
import cv2
import numpy as np
from imagecorruptions import corrupt
from clearml import Task, Dataset, Logger


def add_noise(input_video, output_video, corruption_type='gaussian_noise', severity=1):
    task = Task.init(
        project_name='Image Filter Proccess', 
        task_name='Gaussian Noise Filter',
        task_type=Task.TaskTypes.inference)
    
    # Функция добавляет шум к видео
    cap = cv2.VideoCapture(input_video)
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    print(f"Параметры видео: {total_frames} кадров, {fps} FPS, {width}x{height}")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        corrupted_image = corrupt(frame, corruption_name=corruption_type, severity=severity)
        
        out.write(corrupted_image)
        
        frame_count += 1
        if frame_count == 1 or frame_count % 10 == 0:
            print(f"Обработано: {frame_count}/{total_frames} кадров")
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"Обработка завершена. Файл: {output_video}")

    task.close()

    
def parse_args():
    parser = argparse.ArgumentParser(description="Добавление шума к видеофайлам")
    parser.add_argument(
        "--input_path",
        type=str,
        default="data/input",
        help="Путь к директории с входными файлами (по умолчанию: data/input)"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="data/output",
        help="Путь к директории для выходных файлов (по умолчанию: data/output)"
    )
    parser.add_argument(
        "--input_names",
        type=str,
        nargs="*",
        default=[],
        help="Имена входных файлов для обработки"
    )
    parser.add_argument(
        "--corruption_type",
        type=str,
        default="gaussian_noise",
        help="Тип зашумления (по умолчанию: gaussian_noise)"
    )
    parser.add_argument(
        "--severity",
        type=int,
        default=5,
        help="Уровень зашумления (по умолчанию: 5)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Запустить тестовый режим с тестовым файлом example.mp4"
    )
    return parser.parse_args()


def validate_args(args):
    if args.test:
        args.input_names = ["example.mp4"]

    if not args.input_names:
        print("Предупреждение: список файлов пуст", file=sys.stderr)
        sys.exit(0)

    input_dir = Path(args.input_path)
    if not input_dir.exists():
        print(f"Ошибка: Директория '{args.input_path}' не существует", file=sys.stderr)
        sys.exit(1)

    if not input_dir.is_dir():
        print(f"Ошибка: '{args.input_path}' не является директорией", file=sys.stderr)
        sys.exit(1)

    for file_name in args.input_names:
        input_file = input_dir / file_name
        if not input_file.exists():
            print(f"Ошибка: Файл '{input_file}' не существует", file=sys.stderr)
            sys.exit(1)
        if not input_file.is_file():
            print(f"Ошибка: '{input_file}' не является файлом", file=sys.stderr)
            sys.exit(1)

    output_dir = Path(args.output_path)
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Ошибка: Не удалось создать директорию '{output_dir}': {e}", file=sys.stderr)
            sys.exit(1)

    valid_corruptions = {
        'gaussian_noise', 'shot_noise', 'impulse_noise',
        'defocus_blur', 'motion_blur', 'zoom_blur', 'gaussian_blur',
        'jpeg_compression', 'brightness', 'contrast', 'saturate',
        'spatter', 'speckle_noise'
    }
    if args.corruption_type not in valid_corruptions:
        print(f"Ошибка: Недопустимый тип зашумления '{args.corruption_type}'", file=sys.stderr)
        print(f"Допустимые значения: {', '.join(sorted(valid_corruptions))}", file=sys.stderr)
        sys.exit(1)

    if args.severity < 1 or args.severity > 5:
        print(f"Ошибка: Severity должен быть от 1 до 5 (получено: {args.severity})", file=sys.stderr)
        sys.exit(1)

    return input_dir, output_dir


if __name__ == "__main__":
    args = parse_args()
    input_dir, output_dir = validate_args(args)

    corruption_type = args.corruption_type
    severity = args.severity

    for file_name in args.input_names:
        input_file = input_dir / file_name
        output_file = output_dir / f"{file_name[0:-4]}-{corruption_type}-s{severity}.mp4"
        print(f"Обработка файла: {input_file} -> {output_file}")
        add_noise(
            input_video=str(input_file),
            output_video=str(output_file),
            corruption_type=corruption_type,
            severity=severity
        )
    print("Все файлы успешно обработаны.")