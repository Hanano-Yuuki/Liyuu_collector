import cv2 as cv
from numpy import true_divide
import torch
from facenet_pytorch import MTCNN

def detector(FilePath: str)->bool:
    device = torch.device('cpu')
    mtcnn = MTCNN(keep_all = True, device = device)
    FilePath = cv.imread(FilePath)
    frames = cv.cvtColor(FilePath,cv.COLOR_BGR2RGB)
    boxes,probility = mtcnn.detect(frames)
    if boxes is None:
        return False
    elif probility[0] < 0.95:
        return False
    else:
        return True