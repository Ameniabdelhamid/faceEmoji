"""
This code loads emotion recognition model from a file,
shows a webcam image, recognizes face and it's emotion and draw emotion on the image.
"""
from cv2 import WINDOW_NORMAL

import cv2
from face_detect import find_faces
from image_commons import nparray_as_image, draw_with_alpha


def _load_emoticons(emotions):
    """
    Loads emotions images from graphics folder.
    """
    return [nparray_as_image(cv2.imread('C:\\faceMoji\\graphics\\%s.png' % emotion, -1), mode=None) for emotion in emotions] #emotions: Array of emotions names which returns Array of emotions graphics
                                                                            


def show_webcam_and_run(model, emoticons, window_size=None, window_name='webcam', update_time=10):
    """
    Shows webcam image, detects faces and its emotions in real time and draw emoticons over those faces.
    model: learnt emotion detection model.
    emoticons: list of emotions images.
    window_size: size of webcam image window.
    window_name: name of webcam image window.
    update_time: image update time interval.
    """
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        read_value, webcam_image = vc.read()

    while read_value:
        for normalized_face, (x, y, w, h) in find_faces(webcam_image):
            prediction = model.predict(normalized_face)  # do prediction
            prediction = prediction[0]
            emoj_to_draw = emoticons[prediction]
            draw_with_alpha(webcam_image, emoj_to_draw, (x, y, w, h))

        cv2.imshow(window_name, webcam_image)
        read_value, webcam_image = vc.read()
        key = cv2.waitKey(update_time)

        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow(window_name)


if __name__ == '__main__':
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'surprise']
    emoticons = _load_emoticons(emotions)

    # load model
    fisher_face = cv2.createFisherFaceRecognizer()
    fisher_face.load('C:\\faceMoji\\models\\emotion_detection_model.xml')

    # use learnt model
    window_name = 'MOOD (press ESC to exit)'
    show_webcam_and_run(fisher_face, emoticons, window_size=(1600, 1200), window_name=window_name, update_time=8)
