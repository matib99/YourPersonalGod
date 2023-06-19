import os
import pickle
import numpy as np
import torch
from pti.pti_configs  import paths_config, hyperparameters, global_config
from pti.scripts.run_pti import run_PTI
from moviepy.video.io import ImageSequenceClip

CODE_DIR = "PTI"

image_dir_name = "image"
prepare_room_dir = "./prepare_room"

use_image_online = False
use_multi_id_training = True
global_config.device = "cuda"
#paths_config.e4e = "/content/PTI/pretrained_models/e4e_encode.pt"
#paths_config.input_data_id = "test"
#paths_config.input_data_path = "./ars_electronica"
#paths_config.stylegan2_ada = "./training_results/sg2/god_human/00010-god_human_dataset-rectangle-mirror-shhq4-noaug-resumecustom/network-snapshot-000120.pkl"
#paths_config.checkpoints_dir = "./outputs/pti/checkpoints/"
#paths_config.style_clip_pretrained_mappers = "./PTI/pretrained_models"
hyperparameters.use_locality_regularization = False
step_size = 1.0 / 150.0
fps = 25


def load_generators(model_id, image_name):
    with open(paths_config.stylegan2_ada_shhq, "rb") as f:
        old_G = pickle.load(f)["G_ema"].cuda()

    with open(
        f"{paths_config.checkpoints_dir}model_{model_id}_{image_name}.pkl", "rb"
    ) as f_new:
        new_G = pickle.load(f_new)["G_ema"].cuda()
        #    new_G = torch.load(f_new).cuda()

    return old_G, new_G


def interpolated_latent(w1, w2, alpha):
    return (1 - alpha) * w1 + alpha * w2


def image_from_latents(latent1, latent2, alpha):
    latent = interpolated_latent(latent1, latent2, alpha)
    image = new_G.synthesis(latent, noise_mode="const", force_fp32=True)
    image = (
        (image.permute(0, 2, 3, 1) * 127.5 + 128)
        .clamp(0, 255)
        .to(torch.uint8)
        .detach()
        .cpu()
        .numpy()[0]
    )
    return image, latent


if __name__ == "__main__":
    print("start")
    model_id = run_PTI(use_wandb=False, use_multi_id_training=use_multi_id_training)
    
    print("model loaded")
    generator_type = paths_config.multi_id_model_type
    old_G, new_G = load_generators(model_id, generator_type)
    print("generators loaded")

    latent_codes = []
    latent_files = os.listdir("./outputs/pti/embeddings/test/PTI")
    targetvalue = os.listdir(prepare_room_dir)[0].split(".")[0]
    latent_files.insert(0, latent_files.pop(latent_files.index(targetvalue)))
    for image_name in latent_files:
        w_path_dir = f"{paths_config.embedding_base_dir}/{paths_config.input_data_id}"
        embedding_dir = f"{w_path_dir}/{paths_config.pti_results_keyword}/{image_name}"
        w_pivot = torch.load(f"{embedding_dir}/0.pt")
        latent_codes.append(w_pivot)
    person_latent = latent_codes[0]
    
    print("creating video...")
    # create video of interpolation
    frames = []
    for alpha in np.arange(0, 0.9, step_size):
        (image, latent) = image_from_latents(person_latent, latent_codes[1], alpha)
        frames.append(image)
        if alpha == 0.0:
            for i in range(40):
                frames.append(image)
    for w in latent_codes[2:]:
        for alpha in np.arange(0, 1.0, step_size):
            latent = interpolated_latent(latent, person_latent, alpha / 5.0)
            (image, latent) = image_from_latents(latent, w, alpha)
            frames.append(image)
        for i in range(40):
            frames.append(image)
        #if i % 2 == 0:
    clip = ImageSequenceClip.ImageSequenceClip(frames, fps=fps)
    clip.write_videofile("./outputs/videos/interpolation.mp4")
            #frames = []
    #if len(frames > 0):
        #clip = ImageSequenceClip.ImageSequenceClip(frames, fps=fps)
        #clip.write_videofile(f"./outputs/videos/interpolation_{i.zfill(2)}.mp4")

    #for alpha in np.arange(0, 1.0, step_size):
        #w = 
        #(image, latent) = image_from_latents(latent, w, alpha)
