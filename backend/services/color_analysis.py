import cv2
import numpy as np

from sklearn.cluster import KMeans

COLOR_NAMES = {

    "Black": (0,0,0),
    "White": (255,255,255),
    "Gray": (128,128,128),

    "Red": (255,0,0),
    "Green": (0,255,0),
    "Blue": (0,0,255),

    "Yellow": (255,255,0),
    "Orange": (255,165,0),
    "Brown": (150,75,0),

    "Purple": (128,0,128),
    "Pink": (255,192,203),

    "Cyan": (0,255,255)
}


def nearest_color(rgb):

    rgb=np.array(rgb)

    minimum=None

    color_name=None

    for name,value in COLOR_NAMES.items():

        value=np.array(value)

        distance=np.linalg.norm(rgb-value)

        if minimum is None or distance<minimum:

            minimum=distance

            color_name=name

    return color_name


def detect_colors(image_path,n_colors=5):

    image=cv2.imread(image_path)

    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    pixels=image.reshape((-1,3))

    kmeans=KMeans(

        n_clusters=n_colors,

        random_state=42,

        n_init=10

    )

    kmeans.fit(pixels)

    centers=kmeans.cluster_centers_

    labels=kmeans.labels_

    counts=np.bincount(labels)

    percentages=counts/len(labels)

    result=[]

    for color,percent in zip(centers,percentages):

        name=nearest_color(color)

        result.append({

            "color":name,

            "percentage":round(percent*100,2)

        })

    result=sorted(

        result,

        key=lambda x:x["percentage"],

        reverse=True

    )

    return result