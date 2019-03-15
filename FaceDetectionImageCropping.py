import os
import numpy as np
from autocrop import autocrop as ac
from shutil import copy


def crop(path="./Parsed3_15/", dest="./Cropped128/", pixel=128):
    """
    Crop all of the images in each of the folders in the root directory
    and insert those images into a folder named "crop" in each image folder.

    path (string): Root directory where image folders are located in.
    pixel (int): the output size of one dimension of the cropped images (squares).

    returns None
    """
    reject_dir ="./reject"
    # Make a reject folder
    if os.path.isdir(reject_dir) == False:
        os.mkdir(reject_dir)

    # For every person
    for p_id in os.listdir(path):
        in_dir = path + p_id
        crp_dir = dest + p_id
        err_dir = dest + p_id + "\\reject"

        # Make a new folder if it doesn't exist
        if os.path.isdir(crp_dir) == False:
            os.mkdir(crp_dir)

        # Crop all the images in the folder and store them in "crop"
        ac.main(
            input_d=in_dir,
            output_d=crp_dir,
            reject_d=reject_dir,
            fheight=pixel,
            fwidth=pixel,
            facePercent=90)

def check_emotion(path = "", emotion_list = ["happy", "surprise"]):
    """
    Return true if an emotion in emotion list in present in the folder,
    false otherwise.

    return Boolean
    """

    emotion = False

    for img in os.listdir(path):
        if img.split("_")[0] in emotion_list:
            emotion = True

    return emotion

def train_test_split(path="./Cropped128/", emotion_list = ["happy", "surprise"]):
    """
    Splits data into training and testing folders based on what we emotions
    we can to train out model to detect. Images of people who do not have images
    of the chosen emotions are chosen to be in the test set.

    path (string): root folder of the cropped images
    emotion_list (list of strings): emotions to be used for model training.

    return None
    """

    # If a train and test folder don't exist, create them.
    if os.path.isdir("./train") == False:
        os.mkdir("./train")
    if os.path.isdir("./test") == False:
        os.mkdir("./test")

    # For every person in the root folder
    for p_id in os.listdir(path):
        in_dir = path + p_id
        if check_emotion(in_dir):
            dest = "train"
        else:
            dest = "test"

        # For every emotion in a person folder
        for img in os.listdir(in_dir):
            emo = img.split("_")[0]
            new_dir = dest + "\\" + emo
            # Make an emotion folder if it doesn't exist
            if os.path.isdir(new_dir) == False:
                os.mkdir(new_dir)

            # Copy the image to the new destination
            img_path = in_dir + "\\" + img
            copy(img_path, new_dir + "\\")


def organize(path="./Cropped128/", dest="./OrganizedImages/"):
    """
    Organizes cropped images into emotion folders.

    returns None
    """

    # For every person in the root folder
    for p_id in os.listdir(path):
        in_dir = path + p_id
        # For every emotion in a person folder
        for img in os.listdir(in_dir):
            emo = img.split("_")[0]
            new_dir = dest + "\\" + emo
            # Make an emotion folder if it doesn't exist
            if os.path.isdir(new_dir) == False:
                os.mkdir(new_dir)

            # Rename img
            img_path = in_dir + "\\" + img
            new_path = in_dir + "\\" + img.split(".")[0] + "_" + p_id + ".png"
            os.rename(img_path, new_path)
            # Copy the image to the new destination
            copy(new_path, new_dir + "\\")

if __name__ == "__main__":
    # crop()
    # organize()
    train_test_split()