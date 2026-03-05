import cv2
import numpy as np
from imagecorruptions import corrupt

def add_gaussian_blur_and_noise(input_video, output_video, blur_kernel=(5,5), noise_intensity=25, corruption_type='gaussian_blur', severity=1):
    """
    Добавляет размытие и шум к видео
    """
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
        if frame_count % 10 == 0:
            print(f"Обработано: {frame_count}/{total_frames} кадров")
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"Обработка завершена. Файл: {output_video}")

if __name__ == "__main__":
    input_names = ["spb_gostiny_dvor_001"]
    curruption_names = [
        "gaussian_noise",
        "zoom_blur", 
        "jpeg_compression", 
        "brightness", 
        "saturate", 
        "spatter", 
        "speckle_noise",
        ## "gaussian_blur" 
        "impulse_noise", 
        "shot_noise", 
        "defocus_blur", 
        "motion_blur", 
        "contrast" 
        ]
    severity_number = [1, 2, 3, 4, 5 ]
    for file_name in input_names:
        for corruption_type in curruption_names:
            for severity in severity_number:
                # corruption_type = 'gaussian_noise'
                # severity = 2  # от 1 до 5
                input_file = f'data/input/{file_name}.mp4'  
                output_file = f'data/output/corrupt/{file_name}-{corruption_type}-s{severity}.mp4'
                
                add_gaussian_blur_and_noise(
                    input_video=input_file,
                    output_video=output_file,
                    corruption_type=corruption_type,
                    severity=severity
                )