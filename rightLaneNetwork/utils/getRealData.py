import argparse
import glob
import os.path
import random

import cv2
import wget
from tqdm import tqdm

url = ["https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20171229133444_yaf.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20180108141719_a313.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20171226190358_yaf.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20171229103241_a313.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20170907172845_farmer.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20180104160326_a313.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20180111130129_a313.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20180104160628_a313.video.mp4",
       "https://gateway.ipfs.io/ipfs/QmUbtwQ3QZKmmz5qTjKM3z8LJjsrKBWLUnnzoE5L4M7y7J/logs/20160318162919_penguin.video.mp4",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/665aa4bdc4a71ec38e5d7a0f010da859d3b880160afbd16711fc5cb8b347f8c3",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/a705564425d79cd5b19e2e5869bc13799dcbdd77a18db779720101b3bb337b78",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/dae11959bc83d4267b07e8bcbe289f66cfad055e9cfa96b61c5d73854fd8ef4c",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/6ddf63baf6baa123ba57ab0f73d57e7d9290c3461588980cde0c54863b909bc9",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/4d0910d1e08ede180bfaed33f8b9c4c2904531de50b6ff02d9d6acd5c280245f",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/320d4014191e3ecf190d394e4a7ab8fdc3ba30f29a1ba2d5fafdf4a691928944",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/a2282f9de9beb33ed04e1e515c57a976c2208bb6679d7de29d95ac0941fbc765",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/4f39def9fa6ed245c92b80e6c36d5796a8baff2bf6a30b4e211a570fd9ce3c94",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/bf687477545de6ec014257508869de8ce3c6148584103a091d7f37e717b60fa5",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/0b8cbb2455a867acce843b3e411febc6a85f0a0c2df34e339a57067779144774",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/19f2f99ebe1fe32735d0f26debe4b226a36a298cd7c6267902654a13aa62d173",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/a57ce3f0a472f9418881ea6b3376922401d80312555a7591b24ddf0129c5ea1e",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/391147654af90e1952be3b5540faef546eaea7e234b33994c3e9c2ea15e146b6",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/969cc2012d42854e0744be067eb9c1c7852ba44fe9abc4ca5719b4f6ceaf2f9d",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/6cc8aa29cb3322e070b2f584294d1494e71ca5c08e008ae0f7e28679523b8ac5",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/3edd3057659ebb856058c7002a7e0e43f869db3096b4996fd67e236d24d4bf60",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/8d101d1cf226bdabefaa94f4f58a2db240220037d1e22519208b5aa36326a9a5",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/c813d15bba2f20f45e14ffec479319dd83b143d6d6cae3d6a6ad899642356d8b",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/fa601b43e11f501287bb018c20c57531b0ef5c2046a9183cb519be5096a08f40",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/ea5cc07d706aef4356fd7dfcc74096e32e9050ea84c6ee8ec3d771f775f0585a",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/139efa2b15e7b0bcba93755021798a9296345731dea929e9483e90681396c7da",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/94b5ad144b42e615155b6c05062659fbdb5cde2206c6e7fb9dde6316ebb34157",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/5e9c168ad0a6a62ed6c5a904b65d8eac7f4ebdb6357871932369b6e8798037b0",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/e7848c65a615cf86e523be3b1a16bb697f00b460154ed0468a0205098bd3e98b",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/fdb3bf309aa5e2a7135dd266d3b4a8e97e333c2bafbc13b74ecc636fc1fa5bc6",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/2760095fa4465979f60bb6c9d7799d275c4f9327dd7a874305fc8d0d8b8f639e",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/2024a9f0592e03febf8288c4d14ee4372cb59f3783c701dc2997a8b398a524f6",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/6efd33b8db512158cbc3a89a6325c9918d8e03e1977ddf5ed6b3d2ed0b044cec",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/c94cb0025356d1a481b718872f18cbac56d964e918f0ff3cdf5045926d894f81",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/f7e4fb238bb566139b3ecbb70bfd52a2f4bf17fb4c591fd2ef2aba9d7fc55d55",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/b1812f6f368ed52ca1c42c4aa39eb98540ad6877c445ad49f12fe2dcca497c70",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/c898a4fcc75a5736886b9fb02a1c458febd32aecde862a4d40194ecc311ae2ab",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/9447e0c0423c5eea4b1f78a9cfc9fddb25e05bb025179408a96113615b17384f",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/524e6211e371a99b5c56789a172bd096e32741feb406242c27fdf0060313f50b",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/fee0a40f64a49f20971d2f57ed83796f6bf7efad97bbb8d2ea61c63db6078897",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/1614f25410788af47fa19f43c400b9ce3a3e62ad9a41cad7bb82c9cbf483a3a5",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/ddec1763723b3d487d7e3bb7502884a4c6412ea63c4ec0ae87b209477dfb8645",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/f550e056089f26d9a8d9668cee94e602a02d4a7276eb70c2a30b949429603e69",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/07a48eeeaf5749013715629242de9fa8e6dc1dd2d794ee11e693b43c5935b54b",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/eb6142d2b576c739914e4d9255d88a964766cc47b0ae5c7c1867c72dcaee96cb",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/14d1a6c60c9137008ec3f89f036319376cce7fad3602eed85efe4794cd929c64",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/745b640f574d9767cc544fa2947307ac180dc251dd920c1ce987aa2cd2d02e04",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/1fb655caab73f56b521a07c9815692910f4c3549270fc7af3bd8ee3b63b79128",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/866ef9d05102373cba06acf2ae0eddd48a698708d354dbd0b68245e330624013",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/d61aa2fd01a20145f28f72dcd7bf20f936a5342a1c7959f00a39e736e7f27717",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/5feaf39aede99909c2672a0aa7d00c0ea71b654326ca696b697e227fc4a554a8",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/0e9e0587e391612d5913c2c253fc6c4219493c18113302d5259f7515c804c63b",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/056038dd52172f33bbb8b5f52571355ca12edf7296be4b03f7e92890e89977e5",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/6ddf63baf6baa123ba57ab0f73d57e7d9290c3461588980cde0c54863b909bc9",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/fd9dba351bddee3a70c7809c11952bfb01af42de72b3d14d8e0692bd4209ab1c",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/de6672918721334ff11f61f52401a9634acde30539feb5911559fd25844ce9c9",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/2937b83799fabbf9896eed78bfb937f55dae2706a7c9d21d6002ad5a9be3a1ed",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/8e95680e83eb8c8e74e5393b8701a9cfae4e0669692331dc2614e1efeca7fe20",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/0062c5866d7e67248cbe3adbdc40b2b40afa5fc2e7d76c6e240c911c61c694fd",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/82a52e842f8234c35d0297de7bd4565059f4b711a1a89f10122bc5ac95a595c6",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/f01b6a0569ccb46f4891c7223b74416b32512cdd200d26e2d29d4134b2aa741c",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/02eb34178159c898275a3ff372010d95e2999e9f0164a40f795cda0b8b193770",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/058f9a31bac6e5f5d999f459a16569d01cf2530d6e9c4d42a9ce3c03a27130bc",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/dc4774996854c707e6168a20aae1d9c7b9f8d6de8bbb2d82a06935ff1b86d86f",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/ae199b7170734750d04263e31054ac68f4ed89f9426313630d88375223d1cb0a",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/f067039ca2c7ebce140f216d272d6d55401349cabb51710e6ad85859d4e0a63f",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/cc4c99e5f66f52c6919fce65a2b20b224d282c2021d0ccd9afe932975ee553f3",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/96c345e2985ea2e2308e7ad978a0b85cb803c4c0f3ad30f781f1ebe7c3c40a07",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/fc2119165e42f660bf3c244030fc172fab67c8b1b5cfbd953fa1559c970c4d5c",
       "https://duckietown-ai-driving-olympics-1.s3.amazonaws.com/v3/frankfurt/by-value/sha256/53fda47da15c110b51b982683d9d6325cdc594cb4e0e1d08eb8c22f90ddaf065",
       ]


def download_videos(download_path):
    for i in tqdm(range(len(url))):
        file_path = os.path.join(download_path, f'{i:03d}.mp4')
        wget.download(url[i], file_path)


def saveAsImages(save_path, num_images):
    files = sorted(glob.glob(os.path.join(save_path, '*.mp4')))
    videoset = []

    print("Reading and joining videos")
    for file in tqdm(files):
        cap = cv2.VideoCapture(file)
        while cap.isOpened():
            is_ok, frame = cap.read()
            if not is_ok:
                break
            if frame is not None and frame.size != 0:
                videoset.append(frame)
        cap.release()
        os.remove(file)
    print("Total number of frames = ", len(videoset))

    print("Generating random samples and saving as .png images")
    if num_images >= 0:
        videoset = random.sample(videoset, num_images)

    for i, frame in enumerate(tqdm(videoset)):
        filename = os.path.join(save_path, f"{i:06d}.png")
        cv2.imwrite(filename, frame)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_images', type=int, default=100)
    parser.add_argument('--save_path', type=str, default="./realData")
    parser.add_argument('--as_videos', action='store_true')
    args = parser.parse_args()

    os.makedirs(args.save_path, exist_ok=True)

    print(f"Got arguments: num_images={args.num_images}, save_path={args.save_path}")

    download_videos(args.save_path)
    if not args.as_videos:
        saveAsImages(args.save_path, args.num_images)
