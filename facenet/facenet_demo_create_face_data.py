# function for face detection with mtcnn
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
from os import listdir
from os.path import isdir
from numpy import savez_compressed

# extract a single face from a given photograph


def extract_face(filename, required_size=(160, 160)):

    # load image from file
    image_raw = Image.open(filename)
    # convert to array
    pixels = asarray(image_raw)
    # detect faces in the image
    detector = MTCNN()
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array
# load images and extract faces for all images in a directory


def load_faces(directory):
    faces = list()
    # enumerate files
    for filename in listdir(directory):
        # path
        path = directory + filename
        # get face
        face = extract_face(path)
        # store
        faces.append(face)
    return faces
# load a dataset that contains one subdir for each class that in turn contains images


def load_dataset(directory):
    x, y = list(), list()
    # enumerate folders, on per class
    for subdir in listdir(directory):
        # path
        path = directory + subdir + '/'
        # skip any files that might be in the dir
        if not isdir(path):
            continue
        # load all faces in the subdirectory
        faces = load_faces(path)
        # create labels
        labels = [subdir for _ in range(len(faces))]
        # summarize progress
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # store
        x.extend(faces)
        y.extend(labels)
    return asarray(x), asarray(y)


if __name__ == '__main__':
    import traceback
    folder = 'facenet/5-celebrity-faces-dataset/train/'
    # load train dataset
    trainx, trainy = load_dataset(folder)
    print(trainx.shape, trainy.shape)
    # load test dataset
    testx, testy = load_dataset('facenet/5-celebrity-faces-dataset/val/')
    # save arrays to one file in compressed format
    savez_compressed('facenet/5-celebrity-faces-dataset.npz',
                     trainx, trainy, testx, testy)
