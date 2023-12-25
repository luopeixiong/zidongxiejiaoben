import cv2
import time
import os
from multiprocessing import Pool


def capture_frames(video_info_yuanzhu):
    video_path, output_folder, start_time, interval = video_info_yuanzhu
    cap = cv2.VideoCapture(video_path)

    # 设置视频的帧率
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 计算起始帧和间隔帧数
    start_frame = int(start_time * fps)
    interval_frames = int(interval * fps)

    # 设置当前帧
    current_frame = start_frame

    name = video_path.split('\\')[-1].split('.')[0]

    while True:
        # 设置视频的当前帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

        # 读取当前帧
        ret, frame = cap.read()

        # 如果读取失败，说明到达视频结尾，退出循环
        if not ret:
            break

        # 保存当前帧为图片
        output_path = os.path.join(output_folder, f"{name}_{current_frame // int(fps)}s.jpg")
        cv2.imencode('.jpg', frame)[1].tofile(output_path)
        print(f"Saved frame {current_frame // int(fps)}s to {output_path}")

        # 更新当前帧
        current_frame += interval_frames

    # 释放视频对象
    cap.release()


def main():
    main_path = "D:\\B站下载"
    if not os.path.exists(main_path):
        os.mkdir(main_path)

    output_folder = os.path.join(main_path, "output_frames")
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    os.makedirs(output_folder, exist_ok=True)

    start_time = 3  # 从视频第2秒开始
    interval = 6  # 每隔5秒后换图，一秒切换帧

    video_lst = os.listdir(main_path)

    # 使用多进程池处理多个视频
    with Pool(4) as pool:
        video_info_yuanzhu = [(os.path.join(main_path, video_name), output_folder, start_time, interval) for video_name in video_lst]
        pool.map(capture_frames, video_info_yuanzhu)


if __name__ == "__main__":
    main()
