#!/bin/bash
set -o nounset
set -o errexit


url="rtsp://68.152.51.100/axis-media/media.amp"
#"rtsp://68.152.51.103/axis-media/media.amp"  
 # "rtsp://68.152.51.100/axis-media/media.amp"
num="6"
fre="30" # time interval to extract video
time_limit="30"
start_time_in=$(date +%s)
DIR="./Image"



if [ ! -d $DIR ]
then
    mkdir $DIR
fi
while true # [ $'expr $(date +%s)-$start_time_in' -lt  $time_limit ]
do
	Time=$(date +%s)

	ffmpeg  -i $url -vcodec copy -r 60  -f mp4 -t $fre -y ${DIR}/${Time}.mp4
#cp /Users/Neo/Documents/Programming/Python3/Image/$Time.mp4 /Users/Neo/Documents/Programming/Python3/Image/$Time-1.mp4
done

#ffmpeg -i $url -t $num -r $fre -vsync 1 -qscale 1 -f image2 ${DIR}/$(Time)-%09d.jpg
