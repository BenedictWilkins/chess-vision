# Chess Vision

### Contributors guide

This project aims to convert photographs of chess positions into their digital counter-part. It is an exploration of the latest machine vision techniques. 
There are various things to get involved with:

#### 1. Data collection 

Send us photos or videos of your chess board set up with different positions. By doing so you are consenting to your data being used in this project and other projects. If in doubt see the dataset license on [roboflow](https://app.roboflow.com/chessvision-zekst).

If you know about web scraping, this is also an option. We want as much data as possible. IMPORTANT NOTE: if we go this route we need to respect copyright/licensing, so please only scrape images that are in the public domain. Please also record information about the images (e.g. url and date/time) in a convenient format (TBD).

#### 2. Data cleaning & annotation
We are using [roboflow](roboflow.com) to annotate data.

Roboflow is great for this, but as the dataset gets larger we may reach the "free limit", at which point we will move the dataset to [kaggle](https://www.kaggle.com/).

#### 3. Data augmentation

Artificially expanding the dataset by adding noise, tranformations etc. We need scripts for this!

#### 4. Model selection & training
Some models already exist for this. The most promising - and one that has been used for this purpose in various projects is [yolov8](https://github.com/ultralytics/ultralytics)

Other similar projects:
1. https://chessvision.ai/
2. https://github.com/andrefakhoury/chess-board-recognition
3. https://github.com/krzywilk/chessboard-checker-segmentation
4. https://github.com/Vatsalparsaniya/Yolo-Segmentation-Chess
5. https://github.com/Dilanya/Chess-Pieces-Detection
6. ... no doubt there are more

Most of these projects are working with toy datasets. The models may (or may not) extend to recognising chess peices "in the wild". Our goal is to build a model that will work in the wild for any chess board, lightning conditions, camera, etc. 

#### 5. Model evaluation & testing

Part of this will be test out existing models, on unseen test data (e.g. from the links above). But also to test and evaluate any models trained in this project.

#### 6. Deployment 

The plan is to build a simple mobile app that will run what ever model we train. If you are a mobile dev then please get in touch or have any experience with this, pleae get in touch!
