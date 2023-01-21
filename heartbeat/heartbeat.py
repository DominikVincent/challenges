import numpy as np
import cv2
import skvideo.io  
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

def derivive(arr, dx=2.0):
    print(arr.max())
    return np.diff(arr, axis=0) / dx


def display_video(arr):
    for frame in arr:
        # print("R: ", frame[:,:].min(), " - ", frame[:,:,0].max())
        # print("G: ", frame[:,:,1].min(), " - ", frame[:,:,1].max())
        # print("B: ", frame[:,:,2].min(), " - ", frame[:,:,2].max())
        cv2.imshow("frame", frame)
        if cv2.waitKey(int(1000/24)) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def display_heatmap(arr):
    # frames = []
    # fig = plt.figure()
    print("R: ", arr.min(), " - ", arr.max())

    img = None
    grid_kws = {'width_ratios': (0.9, 0.05), 'wspace': 0.2}
    fig, (ax, cbar_ax) = plt.subplots(1, 2, gridspec_kw = grid_kws, figsize = (10, 8))
    for frame in arr:
        ax.cla()
        sns.heatmap(ax = ax, data = frame, cbar_ax = cbar_ax)

            # img.set_data(frame)
        plt.pause(.1)
        plt.draw()
        # frames.append([sns.heatmap(frame[:,:], animated=True)])

    # ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True,
    #                             repeat_delay=1000)
# ani.save('movie.mp4')
plt.show()

def display_video_from_path(path):
    cap = cv2.VideoCapture(path)

    while(cap.isOpened()):
        ret, frame = cap.read()
        # print(frame.shape)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def min_max_norm(arr):
    return (arr - arr.min()) / (arr.max() - arr.min())

def compute():
    videodata = skvideo.io.vread("straight_green2.mp4").astype(np.float32)[:240,650:1300,430:730,:]
    print(videodata.shape)

    derivative = derivive(videodata)
    print(derivative.shape)
    derivative = min_max_norm(derivative)

    # display_video(derivative)
    # # display_heatmap(derivative)
    # display_heatmap(derivative[:,:,:,0])
    display_video(derivative[:,:,:,0])
    display_video(derivative[:,:,:,1])
    display_video(derivative[:,:,:,2])
    # display_heatmap(videodata[:,:,:,0])

if __name__ == "__main__":
    compute()