# TA CAR
![screenshot](https://github.com/joonaspessi/tacar/blob/master/resources/screenshot.PNG)
Utility software for capturing training data for `TÄ Solutions self driving car`

## Introduction

This highly customised utility software captures screenshots together with game controller.

## Usage

1. Select directory for log data
2. Start recording. Recording can be stopped and restored during session

## Data format
Controller values are stored to json format as record_{id} in following format:

### format
```json
{
    "cam/image_array": "shot_{0}.png",
    "user/throttle": 0,
    "user/steering": 0,
    "user/brake": 0,
    "user/mode": "user"
}
```
### Screencaptures

Screencaptures are saved as shot_{id}.png

 
