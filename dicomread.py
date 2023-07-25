import cv2
import pydicom
import numpy as np

def adjust_window(img, window_center, window_width):
    # 计算窗口范围
    window_min = window_center - window_width/2
    window_max = window_center + window_width/2

    # 将像素值限制在窗宽窗位范围内
    windowed_image = np.clip(img, window_min, window_max)

    # 将像素值映射到0-255的范围
    windowed_image = ((windowed_image - window_min) / (window_max - window_min) * 255).astype(np.uint8)

    return windowed_image

def update_window_values(*args):
    # 从滑动条获取窗宽和窗位的值
    window_width = cv2.getTrackbarPos('Window Width', 'DICOM Image')
    window_center = cv2.getTrackbarPos('Window Center', 'DICOM Image')

    # 调整窗宽窗位
    windowed_image = adjust_window(img, window_center, window_width)

    # 显示调整后的图像
    cv2.imshow('DICOM Image', windowed_image)

# 读取 DICOM 文件
dcm = pydicom.dcmread("C:\\Users\\ASUS\\Desktop\\dicom\\TestPattern_RGB.dcm")

# 获取图像数据
img = dcm.pixel_array

# DICOM 文件可能使用了不同的缩放或窗口，所以我们需要将其转换为 OpenCV 可以处理的格式
img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# 创建窗口和滑动条
cv2.namedWindow('DICOM Image')
cv2.createTrackbar('Window Center', 'DICOM Image', int(img.max()/2), int(img.max()), update_window_values)
cv2.createTrackbar('Window Width', 'DICOM Image', int(img.max()), int(img.max()), update_window_values)

# 初始化调整窗宽窗位
update_window_values()

# 等待按下ESC键退出程序
while cv2.waitKey(0) != 27:
    pass

# 关闭窗口
cv2.destroyAllWindows()
