from moviepy.editor import VideoFileClip
import ffmpeg

base = "C:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\ArtGenerationDriver\\data\\artGenerationOutput_0.mov"
prep = "C:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/BackEndCommandInterface/data/artGen.mp4"
done = "C:/Users/pratt/Downloads/test.mp4"


ffmpeg.input(base).output(prep).overwrite_output().run();

file = VideoFileClip(prep);

file.write_videofile(done);
